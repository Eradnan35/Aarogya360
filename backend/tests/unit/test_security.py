import pytest

from backend.app.core.security import (
    create_access_token,
    decode_token,
    generate_refresh_token,
    hash_password,
    hash_token,
    verify_password,
)
from uuid import uuid4


def test_password_hashing_roundtrip():
    plain = "MySecurePassword123"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed)
    assert not verify_password("wrong-password", hashed)


def test_refresh_token_hash_is_deterministic():
    token = generate_refresh_token()
    assert hash_token(token) == hash_token(token)
    assert hash_token(token) != hash_token(generate_refresh_token())


def test_access_token_encode_decode():
    user_id = uuid4()
    clinic_id = uuid4()
    session_id = uuid4()

    token = create_access_token(
        user_id=user_id,
        clinic_id=clinic_id,
        role_name="admin",
        session_id=session_id,
    )
    claims = decode_token(token)
    assert claims["sub"] == str(user_id)
    assert claims["clinic_id"] == str(clinic_id)
    assert claims["type"] == "access"
    assert claims["role"] == "admin"
