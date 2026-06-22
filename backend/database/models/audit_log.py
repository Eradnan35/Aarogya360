import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, GUID

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    actor_user_id = Column(GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String, nullable=False)  # create, update, delete, login, etc.
    entity_type = Column(String, nullable=False, index=True)  # Appointment, User, Patient, etc.
    entity_id = Column(GUID, nullable=True, index=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    clinic = relationship("Clinic", back_populates="audit_logs")
    actor = relationship("User", foreign_keys=[actor_user_id])
