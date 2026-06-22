import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Table, Text, JSON, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, SoftDeleteMixin, GUID

# Association table for role permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", GUID, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", GUID, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")
    users = relationship("User", back_populates="role")

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")

class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("clinic_id", "email", name="uq_user_clinic_email"),
    )

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(GUID, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    password_hash = Column(Text, nullable=False)
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login_at = Column(DateTime, nullable=True)
    
    created_by_id = Column("created_by", GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by_id = Column("updated_by", GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    clinic = relationship("Clinic", back_populates="users")
    role = relationship("Role", back_populates="users")
    
    # Self-referencing relationships
    creator = relationship("User", foreign_keys=[created_by_id], remote_side=[id])
    updater = relationship("User", foreign_keys=[updated_by_id], remote_side=[id])
    
    mfa = relationship("UserMFA", uselist=False, back_populates="user", cascade="all, delete-orphan")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    doctor_profile = relationship("Doctor", uselist=False, back_populates="user", cascade="all, delete-orphan")

class UserMFA(Base, TimestampMixin):
    __tablename__ = "user_mfa"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    secret = Column(Text, nullable=False)
    backup_codes = Column(JSON, nullable=True)
    verified_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="mfa")

class StaffInvitation(Base):
    __tablename__ = "staff_invitations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(GUID, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    email = Column(String, nullable=False, index=True)
    invite_token = Column(Text, nullable=False)
    status = Column(String, default="pending", nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    token_hash = Column(Text, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="refresh_tokens")

class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    device_name = Column(String, nullable=True)
    device_type = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)
    last_activity_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="sessions")
