from __future__ import annotations

from typing import Optional
from uuid import UUID

from backend.app.auth.repository import AuthRepository
from backend.app.auth.schemas import (
    ChangePasswordRequest,
    LoginRequest,
    LogoutRequest,
    MeResponse,
    RefreshRequest,
    RegisterRequest,
    RegisterResponse,
    RoleInfo,
    TokenResponse,
)
from backend.app.core.config import Settings, get_settings
from backend.app.core.exceptions import InactiveUserError, InvalidCredentialsError, TokenError
from backend.app.core.security import (
    create_access_token,
    generate_refresh_token,
    get_refresh_token_expiry,
    hash_password,
    hash_token,
    verify_password,
)
from backend.app.core.datetime_utils import utc_now
from backend.database.models.user import User


class AuthService:
    def __init__(
        self,
        repository: AuthRepository,
        settings: Optional[Settings] = None,
    ) -> None:
        self._repo = repository
        self._settings = settings or get_settings()

    async def login(
        self,
        payload: LoginRequest,
        *,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_name: Optional[str] = None,
        device_type: Optional[str] = None,
    ) -> TokenResponse:
        user = await self._repo.get_user_by_email_and_clinic(
            email=payload.email,
            clinic_id=payload.clinic_id,
        )
        if user is None or not verify_password(payload.password, user.password_hash):
            raise InvalidCredentialsError()

        self._ensure_user_active(user)

        now = utc_now()
        refresh_expires = get_refresh_token_expiry(self._settings)

        session = await self._repo.create_user_session(
            user_id=user.id,
            expires_at=refresh_expires,
            device_name=device_name,
            device_type=device_type,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        refresh_token = generate_refresh_token()
        await self._repo.create_refresh_token(
            user_id=user.id,
            token_hash=hash_token(refresh_token),
            expires_at=refresh_expires,
        )
        await self._repo.update_last_login(user.id, now)

        access_token = create_access_token(
            user_id=user.id,
            clinic_id=user.clinic_id,
            role_name=user.role.name if user.role else None,
            session_id=session.id,
            settings=self._settings,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=self._settings.access_token_expire_minutes * 60,
        )

    async def refresh(self, payload: RefreshRequest) -> TokenResponse:
        token_hash = hash_token(payload.refresh_token)
        stored = await self._repo.get_valid_refresh_token(token_hash)
        if stored is None or stored.user is None:
            raise TokenError("Invalid or expired refresh token")

        user = stored.user
        self._ensure_user_active(user)

        await self._repo.revoke_refresh_token(stored.id)

        refresh_expires = get_refresh_token_expiry(self._settings)
        new_refresh_token = generate_refresh_token()
        await self._repo.create_refresh_token(
            user_id=user.id,
            token_hash=hash_token(new_refresh_token),
            expires_at=refresh_expires,
        )

        active_session = await self._repo.get_latest_active_session_for_user(user.id)
        if active_session is None:
            raise TokenError("No active session found")

        await self._repo.touch_session(active_session.id)

        access_token = create_access_token(
            user_id=user.id,
            clinic_id=user.clinic_id,
            role_name=user.role.name if user.role else None,
            session_id=active_session.id,
            settings=self._settings,
        )

        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
            expires_in=self._settings.access_token_expire_minutes * 60,
        )

    async def logout(
        self,
        user: User,
        payload: LogoutRequest,
        *,
        session_id: Optional[UUID] = None,
    ) -> None:
        if payload.refresh_token:
            token_hash = hash_token(payload.refresh_token)
            stored = await self._repo.get_valid_refresh_token(token_hash)
            if stored and stored.user_id == user.id:
                await self._repo.revoke_refresh_token(stored.id)

        if session_id:
            await self._repo.expire_session(session_id)

    async def authenticate_access_token(self, token: str) -> User:
        try:
            claims = self._decode_access_token(token)
        except ValueError as exc:
            raise TokenError(str(exc)) from exc

        if claims.get("type") != "access":
            raise TokenError("Invalid token type")

        user_id = UUID(claims["sub"])
        clinic_id = UUID(claims["clinic_id"])
        session_id = UUID(claims["session_id"])

        user = await self._repo.get_user_by_id_and_clinic(user_id, clinic_id)
        if user is None:
            raise TokenError("User not found")

        self._ensure_user_active(user)

        session = await self._repo.get_active_session(session_id, user_id)
        if session is None:
            raise TokenError("Session expired or revoked")

        await self._repo.touch_session(session_id)

        return user

    def build_me_response(self, user: User, session_id: Optional[UUID] = None) -> MeResponse:
        permissions = (
            [perm.name for perm in user.role.permissions]
            if user.role and user.role.permissions
            else []
        )
        role_info = RoleInfo.model_validate(user.role) if user.role else None
        base = MeResponse.model_validate(user)
        base.role = role_info
        base.permissions = permissions
        base.session_id = session_id
        return base

    def _decode_access_token(self, token: str) -> dict:
        from backend.app.core.security import decode_token

        return decode_token(token, self._settings)

    @staticmethod
    def _ensure_user_active(user: User) -> None:
        if not user.is_active or user.deleted_at is not None:
            raise InactiveUserError()

    async def register(self, payload: RegisterRequest) -> RegisterResponse:
        role_name = "Admin"
        role = await self._repo.get_role_by_name(role_name)
        if not role:
            raise ValueError(f"Role '{role_name}' not found in the system.")

        password_hash = hash_password(payload.password, self._settings)
        clinic, user = await self._repo.create_clinic_and_owner(
            clinic_name=payload.clinic_name,
            clinic_phone=payload.clinic_phone,
            clinic_email=payload.clinic_email,
            user_name=payload.user_name,
            user_email=payload.user_email,
            password_hash=password_hash,
            role_id=role.id,
        )

        me_response = self.build_me_response(user)
        return RegisterResponse(user=me_response, clinic_id=clinic.id)

    async def change_password(self, user: User, payload: ChangePasswordRequest) -> None:
        if not verify_password(payload.current_password, user.password_hash):
            raise InvalidCredentialsError()

        new_password_hash = hash_password(payload.new_password, self._settings)
        await self._repo.update_user_password(user.id, new_password_hash)

