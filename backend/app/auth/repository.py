from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.app.core.datetime_utils import utc_now

from backend.database.models.user import RefreshToken, Role, User, UserSession
from backend.database.models.clinic import Clinic

class AuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_user_by_email_and_clinic(
        self,
        email: str,
        clinic_id: UUID,
    ) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.role).selectinload(Role.permissions))
            .where(
                User.email == email,
                User.clinic_id == clinic_id,
            )
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id_and_clinic(
        self,
        user_id: UUID,
        clinic_id: UUID,
    ) -> Optional[User]:
        stmt = (
            select(User)
            .options(selectinload(User.role).selectinload(Role.permissions))
            .where(
                User.id == user_id,
                User.clinic_id == clinic_id,
                User.deleted_at.is_(None),
            )
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_last_login(self, user_id: UUID, login_at: datetime) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(last_login_at=login_at, updated_at=login_at)
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)

    async def create_user_session(
        self,
        *,
        user_id: UUID,
        expires_at: datetime,
        device_name: Optional[str] = None,
        device_type: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> UserSession:
        now = utc_now()
        session = UserSession(
            id=uuid4(),
            user_id=user_id,
            device_name=device_name,
            device_type=device_type,
            ip_address=ip_address,
            user_agent=user_agent,
            last_activity_at=now,
            expires_at=expires_at,
            created_at=now,
        )
        self._session.add(session)
        await self._session.flush()
        return session

    async def get_latest_active_session_for_user(
        self,
        user_id: UUID,
    ) -> Optional[UserSession]:
        now = utc_now()
        stmt = (
            select(UserSession)
            .where(
                UserSession.user_id == user_id,
                UserSession.expires_at > now,
            )
            .order_by(UserSession.last_activity_at.desc())
            .limit(1)
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_active_session(
        self,
        session_id: UUID,
        user_id: UUID,
    ) -> Optional[UserSession]:
        now = utc_now()
        stmt = (
            select(UserSession)
            .where(
                UserSession.id == session_id,
                UserSession.user_id == user_id,
                UserSession.expires_at > now,
            )
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def touch_session(self, session_id: UUID) -> None:
        now = utc_now()
        stmt = (
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(last_activity_at=now)
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)

    async def expire_session(self, session_id: UUID) -> None:
        now = utc_now()
        stmt = (
            update(UserSession)
            .where(UserSession.id == session_id)
            .values(expires_at=now, last_activity_at=now)
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)

    async def create_refresh_token(
        self,
        *,
        user_id: UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:
        token = RefreshToken(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=utc_now(),
        )
        self._session.add(token)
        await self._session.flush()
        return token

    async def get_valid_refresh_token(
        self,
        token_hash: str,
    ) -> Optional[RefreshToken]:
        now = utc_now()
        stmt = (
            select(RefreshToken)
            .options(
                selectinload(RefreshToken.user)
                .selectinload(User.role)
                .selectinload(Role.permissions)
            )
            .where(
                RefreshToken.token_hash == token_hash,
                RefreshToken.revoked_at.is_(None),
                RefreshToken.expires_at > now,
            )
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def revoke_refresh_token(self, token_id: UUID) -> None:
        now = utc_now()
        stmt = (
            update(RefreshToken)
            .where(RefreshToken.id == token_id)
            .values(revoked_at=now)
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)

    async def revoke_refresh_tokens_for_user(self, user_id: UUID) -> None:
        now = utc_now()
        stmt = (
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked_at.is_(None),
            )
            .values(revoked_at=now)
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)

    async def get_role_by_name(self, role_name: str) -> Optional[Role]:
        stmt = select(Role).where(Role.name == role_name)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_clinic_and_owner(
        self,
        clinic_name: str,
        clinic_phone: str,
        clinic_email: str,
        user_name: str,
        user_email: str,
        password_hash: str,
        role_id: UUID,
    ) -> tuple[Clinic, User]:
        clinic = Clinic(
            id=uuid4(),
            name=clinic_name,
            phone=clinic_phone,
            email=clinic_email,
        )
        self._session.add(clinic)
        
        user = User(
            id=uuid4(),
            clinic_id=clinic.id,
            role_id=role_id,
            name=user_name,
            email=user_email,
            password_hash=password_hash,
            is_active=True,
        )
        self._session.add(user)
        await self._session.flush()
        
        # Load the role and permissions for the returned user
        stmt = (
            select(User)
            .options(selectinload(User.role).selectinload(Role.permissions))
            .where(User.id == user.id)
            .execution_options(ignore_tenant=True)
        )
        result = await self._session.execute(stmt)
        return clinic, result.scalar_one()

    async def update_user_password(self, user_id: UUID, password_hash: str) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(password_hash=password_hash, updated_at=utc_now())
            .execution_options(ignore_tenant=True)
        )
        await self._session.execute(stmt)
