from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Request, status

from backend.app.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    MeResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from backend.app.auth.service import AuthService
from backend.app.core.dependencies import get_auth_service, get_client_ip, get_current_active_user
from backend.app.core.security import decode_token
from backend.app.core.config import get_settings
from backend.database.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _extract_session_id_from_token(request: Request) -> Optional[UUID]:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        return None
    token = auth_header.split(" ", 1)[1]
    try:
        claims = decode_token(token, get_settings())
        session_id = claims.get("session_id")
        return UUID(session_id) if session_id else None
    except ValueError:
        return None


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    payload: LoginRequest,
    request: Request,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    return await auth_service.login(
        payload,
        ip_address=get_client_ip(request),
        user_agent=request.headers.get("User-Agent"),
    )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_tokens(
    payload: RefreshRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> TokenResponse:
    return await auth_service.refresh(payload)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    payload: LogoutRequest,
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    session_id = _extract_session_id_from_token(request)
    await auth_service.logout(current_user, payload, session_id=session_id)


@router.get("/me", response_model=MeResponse, status_code=status.HTTP_200_OK)
async def get_me(
    request: Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> MeResponse:
    session_id = _extract_session_id_from_token(request)
    return auth_service.build_me_response(current_user, session_id=session_id)


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> RegisterResponse:
    return await auth_service.register(payload)


@router.post("/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    payload: ChangePasswordRequest,
    current_user: Annotated[User, Depends(get_current_active_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> None:
    await auth_service.change_password(current_user, payload)
