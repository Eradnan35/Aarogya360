import uuid
from sqlalchemy import Column, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, GUID

class NotificationPreference(Base, TimestampMixin):
    __tablename__ = "notification_preferences"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    patient_id = Column(GUID, ForeignKey("patients.id", ondelete="CASCADE"), unique=True, nullable=False)
    email_opt_in = Column(Boolean, default=True, nullable=False)
    sms_opt_in = Column(Boolean, default=True, nullable=False)
    whatsapp_opt_in = Column(Boolean, default=True, nullable=False)
    marketing_opt_in = Column(Boolean, default=False, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="notification_preferences")
