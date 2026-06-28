from __future__ import annotations

from typing import Annotated, Callable, Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.auth.repository import AuthRepository
from backend.app.auth.service import AuthService
from backend.app.core.exceptions import PermissionDeniedError, TokenError
from backend.app.core.tenant import set_tenant_from_jwt
from backend.database.models.user import User
from backend.database.session import get_async_session

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_repository(
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthRepository:
    return AuthRepository(db)


def get_auth_service(
    repository: Annotated[AuthRepository, Depends(get_auth_repository)],
) -> AuthService:
    return AuthService(repository)


async def get_current_user(
    credentials: Annotated[Optional[HTTPAuthorizationCredentials], Depends(bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise TokenError("Missing or invalid authorization header")

    user = await auth_service.authenticate_access_token(credentials.credentials)
    set_tenant_from_jwt(user.clinic_id)
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


def require_roles(*roles: str) -> Callable:
    """Dependency factory: user must have one of the given roles."""

    async def _checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        role_name = current_user.role.name if current_user.role else None
        if role_name not in roles:
            raise PermissionDeniedError(
                message=f"Required role: {', '.join(roles)}",
            )
        return current_user

    return _checker


def require_permissions(*permissions: str) -> Callable:
    """Dependency factory: user must have all listed permissions."""

    async def _checker(
        current_user: Annotated[User, Depends(get_current_active_user)],
    ) -> User:
        user_permissions = {
            perm.name for perm in (current_user.role.permissions if current_user.role else [])
        }
        missing = [perm for perm in permissions if perm not in user_permissions]
        if missing:
            raise PermissionDeniedError(
                message=f"Missing permissions: {', '.join(missing)}",
            )
        return current_user

    return _checker


def get_client_ip(request: Request) -> Optional[str]:
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None
