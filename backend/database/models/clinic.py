import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, DateTime, ForeignKey, Time, Text, JSON
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, SoftDeleteMixin, GUID

class SubscriptionPlan(Base, TimestampMixin):
    __tablename__ = "subscription_plans"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    max_doctors = Column(Integer, nullable=False, default=1)
    max_patients = Column(Integer, nullable=False, default=100)
    price_monthly = Column(Numeric(10, 2), nullable=False, default=0.0)
    features = Column(JSON, nullable=True)

    # Relationships
    clinics = relationship("Clinic", back_populates="subscription_plan")

class Clinic(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "clinics"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    address_line_1 = Column(Text, nullable=True)
    address_line_2 = Column(Text, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    country = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    gstin = Column(String, nullable=True)
    timezone = Column(String, nullable=True, default="UTC")
    logo_url = Column(Text, nullable=True)
    subscription_plan_id = Column(GUID, ForeignKey("subscription_plans.id"), nullable=True)
    trial_starts_at = Column(DateTime, nullable=True)
    trial_ends_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    subscription_plan = relationship("SubscriptionPlan", back_populates="clinics")
    working_hours = relationship("ClinicWorkingHours", back_populates="clinic", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="clinic", cascade="all, delete-orphan")
    users = relationship("User", back_populates="clinic", cascade="all, delete-orphan")
    doctors = relationship("Doctor", back_populates="clinic", cascade="all, delete-orphan")
    patients = relationship("Patient", back_populates="primary_clinic", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="clinic", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="clinic", cascade="all, delete-orphan")

class ClinicWorkingHours(Base, TimestampMixin):
    __tablename__ = "clinic_working_hours"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)

    # Relationships
    clinic = relationship("Clinic", back_populates="working_hours")

class Department(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "departments"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # Relationships
    clinic = relationship("Clinic", back_populates="departments")
    doctors = relationship("Doctor", back_populates="department")
