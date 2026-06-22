import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, SoftDeleteMixin, GUID

class Appointment(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "appointments"
    __table_args__ = (
        UniqueConstraint("doctor_id", "slot_start", name="uq_doctor_slot_start"),
        UniqueConstraint("idempotency_key", name="uq_appointment_idempotency_key"),
    )

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    doctor_id = Column(GUID, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False)
    patient_id = Column(GUID, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    slot_start = Column(DateTime, nullable=False)
    slot_end = Column(DateTime, nullable=False)
    token_number = Column(Integer, nullable=True)
    queue_position = Column(Integer, nullable=True)
    checked_in_at = Column(DateTime, nullable=True)
    called_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    idempotency_key = Column(String, nullable=True)
    status = Column(String, default="scheduled", nullable=False)  # scheduled, checked_in, called, completed, cancelled, no_show
    notes = Column(Text, nullable=True)
    
    created_by_id = Column("created_by", GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    updated_by_id = Column("updated_by", GUID, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    # Relationships
    clinic = relationship("Clinic", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")
    
    creator = relationship("User", foreign_keys=[created_by_id])
    updater = relationship("User", foreign_keys=[updated_by_id])
