import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, declared_attr

Base = declarative_base()

import uuid as _uuid_lib
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID as pgUUID

class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type, otherwise CHAR(36), keeping as UUID objects.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(pgUUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == "postgresql":
            return str(value)
        else:
            if not isinstance(value, _uuid_lib.UUID):
                return str(_uuid_lib.UUID(value))
            else:
                return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, _uuid_lib.UUID):
                return _uuid_lib.UUID(value)
            return value


class TimestampMixin:
    """Mixin for tracking creation and update timestamps."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class SoftDeleteMixin:
    """Mixin for tracking soft deletion of records."""
    deleted_at = Column(DateTime, nullable=True)

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

# Import all models here so that they are registered on Base.metadata
# for Alembic or create_all()
from backend.database.models.clinic import SubscriptionPlan, Clinic, ClinicWorkingHours, Department
from backend.database.models.user import Role, Permission, role_permissions, User, UserMFA, StaffInvitation, RefreshToken, UserSession
from backend.database.models.doctor import Doctor, DoctorAvailability, DoctorLeave
from backend.database.models.patient import Patient, ClinicPatient, GuardianConsent
from backend.database.models.notification import NotificationPreference
from backend.database.models.appointment import Appointment
from backend.database.models.audit_log import AuditLog

