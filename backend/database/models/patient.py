import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, SoftDeleteMixin, GUID

class Patient(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "patients"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    primary_clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="SET NULL"), nullable=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True, index=True)
    email = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    blood_group = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    abha_id = Column(String, unique=True, nullable=True, index=True)
    qr_code = Column(String, unique=True, nullable=True)
    is_minor = Column(Boolean, default=False, nullable=False)

    # Relationships
    primary_clinic = relationship("Clinic", back_populates="patients")
    clinics_association = relationship("ClinicPatient", back_populates="patient", cascade="all, delete-orphan")
    notification_preferences = relationship("NotificationPreference", uselist=False, back_populates="patient", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")
    
    # Guardian consent relationships (self-referencing via junction table)
    consents_as_minor = relationship("GuardianConsent", foreign_keys="[GuardianConsent.minor_patient_id]", back_populates="minor_patient")
    consents_as_guardian = relationship("GuardianConsent", foreign_keys="[GuardianConsent.guardian_patient_id]", back_populates="guardian_patient")

class ClinicPatient(Base):
    __tablename__ = "clinic_patients"

    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), primary_key=True)
    patient_id = Column(GUID, ForeignKey("patients.id", ondelete="CASCADE"), primary_key=True)
    status = Column(String, default="active", nullable=False)
    linked_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="clinics_association")

class GuardianConsent(Base):
    __tablename__ = "guardian_consents"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    minor_patient_id = Column(GUID, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    guardian_patient_id = Column(GUID, ForeignKey("patients.id", ondelete="CASCADE"), nullable=False, index=True)
    consent_type = Column(String, nullable=False)
    granted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)

    # Relationships
    minor_patient = relationship("Patient", foreign_keys=[minor_patient_id], back_populates="consents_as_minor")
    guardian_patient = relationship("Patient", foreign_keys=[guardian_patient_id], back_populates="consents_as_guardian")
