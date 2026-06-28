import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any, Optional
from uuid import UUID

import jwt
from passlib.context import CryptContext

from backend.app.core.config import Settings, get_settings
from backend.app.core.datetime_utils import utc_now

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain_password: str, settings: Optional[Settings] = None) -> str:
    settings = settings or get_settings()
    return pwd_context.hash(plain_password, rounds=settings.bcrypt_rounds)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(48)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_access_token(
    *,
    user_id: UUID,
    clinic_id: UUID,
    role_name: Optional[str],
    session_id: UUID,
    settings: Optional[Settings] = None,
    extra_claims: Optional[dict[str, Any]] = None,
) -> str:
    settings = settings or get_settings()
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "clinic_id": str(clinic_id),
        "role": role_name,
        "session_id": str(session_id),
        "type": "access",
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)
    return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str, settings: Optional[Settings] = None) -> dict[str, Any]:
    settings = settings or get_settings()
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["exp", "sub", "type"]},
        )
    except jwt.ExpiredSignatureError as exc:
        raise ValueError("Token has expired") from exc
    except jwt.InvalidTokenError as exc:
        raise ValueError("Invalid token") from exc


def get_refresh_token_expiry(settings: Optional[Settings] = None) -> datetime:
    settings = settings or get_settings()
    return utc_now() + timedelta(days=settings.refresh_token_expire_days)
