from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4

from backend.database.schemas import UserResponse


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    clinic_id: UUID4


class RefreshRequest(BaseModel):
    refresh_token: str = Field(..., min_length=32)


class LogoutRequest(BaseModel):
    refresh_token: Optional[str] = Field(None, min_length=32)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token lifetime in seconds")


class RoleInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class MeResponse(UserResponse):
    role: Optional[RoleInfo] = None
    permissions: list[str] = []
    session_id: Optional[UUID4] = None
    last_login_at: Optional[datetime] = None


class RegisterRequest(BaseModel):
    clinic_name: str = Field(..., min_length=2, max_length=200)
    clinic_phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    clinic_email: EmailStr
    user_name: str = Field(..., min_length=2, max_length=150)
    user_email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class RegisterResponse(BaseModel):
    user: MeResponse
    clinic_id: UUID4


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=1, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)
