import pytest
from httpx import ASGITransport, AsyncClient
from uuid import uuid4

from backend.app.core.security import hash_password
from backend.app.main import app
from backend.database.database import SessionLocal
from backend.database.models.clinic import Clinic
from backend.database.models.user import Permission, Role, User


@pytest.fixture(scope="module")
def seed_auth_data():
    suffix = uuid4().hex[:8]
    clinic_id = uuid4()
    role_id = uuid4()
    user_id = uuid4()
    perm_id = uuid4()
    password = "SecurePass123"

    db = SessionLocal()
    try:
        clinic = Clinic(
            id=clinic_id,
            name=f"Test Clinic {suffix}",
            email=f"clinic-{suffix}@test.com",
            phone="+919876543210",
            is_active=True,
        )
        permission = Permission(
            id=perm_id,
            name=f"patients:read:{suffix}",
            description="Read patients",
        )
        role = Role(
            id=role_id,
            name=f"admin-{suffix}",
            description="Administrator",
        )
        role.permissions.append(permission)

        user = User(
            id=user_id,
            clinic_id=clinic_id,
            role_id=role_id,
            name="Test Admin",
            email=f"admin-{suffix}@test.com",
            phone="+919876543211",
            password_hash=hash_password(password),
            is_active=True,
        )

        db.add_all([clinic, permission, role, user])
        db.commit()

        yield {
            "clinic_id": clinic_id,
            "user_id": user_id,
            "email": f"admin-{suffix}@test.com",
            "password": password,
            "role": f"admin-{suffix}",
            "permission": f"patients:read:{suffix}",
        }
    finally:
        db.close()


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_login_success(client, seed_auth_data):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": seed_auth_data["email"],
            "password": seed_auth_data["password"],
            "clinic_id": str(seed_auth_data["clinic_id"]),
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 900


@pytest.mark.asyncio
async def test_login_invalid_credentials(client, seed_auth_data):
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": seed_auth_data["email"],
            "password": "WrongPassword123",
            "clinic_id": str(seed_auth_data["clinic_id"]),
        },
    )
    assert response.status_code == 401
    assert response.json()["error"] == "INVALID_CREDENTIALS"


@pytest.mark.asyncio
async def test_me_endpoint(client, seed_auth_data):
    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": seed_auth_data["email"],
            "password": seed_auth_data["password"],
            "clinic_id": str(seed_auth_data["clinic_id"]),
        },
    )
    token = login.json()["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["email"] == seed_auth_data["email"]
    assert body["role"]["name"] == seed_auth_data["role"]
    assert seed_auth_data["permission"] in body["permissions"]


@pytest.mark.asyncio
async def test_refresh_token_rotation(client, seed_auth_data):
    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": seed_auth_data["email"],
            "password": seed_auth_data["password"],
            "clinic_id": str(seed_auth_data["clinic_id"]),
        },
    )
    old_refresh = login.json()["refresh_token"]

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert refresh.status_code == 200
    new_tokens = refresh.json()
    assert new_tokens["refresh_token"] != old_refresh

    # Old refresh token must be revoked
    reuse = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": old_refresh},
    )
    assert reuse.status_code == 401


@pytest.mark.asyncio
async def test_logout(client, seed_auth_data):
    login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": seed_auth_data["email"],
            "password": seed_auth_data["password"],
            "clinic_id": str(seed_auth_data["clinic_id"]),
        },
    )
    tokens = login.json()

    logout = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert logout.status_code == 204

    refresh = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": tokens["refresh_token"]},
    )
    assert refresh.status_code == 401


@pytest.mark.asyncio
async def test_inactive_user_blocked(client, seed_auth_data):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == seed_auth_data["user_id"]).one()
        user.is_active = False
        db.commit()

        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": seed_auth_data["email"],
                "password": seed_auth_data["password"],
                "clinic_id": str(seed_auth_data["clinic_id"]),
            },
        )
        assert response.status_code == 401
        assert response.json()["error"] == "INACTIVE_USER"
    finally:
        user.is_active = True
        db.commit()
        db.close()
