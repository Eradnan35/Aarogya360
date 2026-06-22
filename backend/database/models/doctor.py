import uuid
from sqlalchemy import Column, String, Integer, Numeric, ForeignKey, Time, Date, Text
from sqlalchemy.orm import relationship
from backend.database.models.base import Base, TimestampMixin, SoftDeleteMixin, GUID

class Doctor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "doctors"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    clinic_id = Column(GUID, ForeignKey("clinics.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(GUID, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    department_id = Column(GUID, ForeignKey("departments.id", ondelete="SET NULL"), nullable=True)
    specialization = Column(String, nullable=True)
    qualification = Column(String, nullable=True)
    registration_number = Column(String, unique=True, nullable=False)
    consultation_fee = Column(Numeric(10, 2), nullable=False, default=0.0)
    experience_years = Column(Integer, nullable=True)

    # Relationships
    clinic = relationship("Clinic", back_populates="doctors")
    user = relationship("User", back_populates="doctor_profile")
    department = relationship("Department", back_populates="doctors")
    availability = relationship("DoctorAvailability", back_populates="doctor", cascade="all, delete-orphan")
    leaves = relationship("DoctorLeave", back_populates="doctor", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")

class DoctorAvailability(Base, TimestampMixin):
    __tablename__ = "doctor_availability"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    doctor_id = Column(GUID, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    day_of_week = Column(Integer, nullable=False)  # 0 = Monday, 6 = Sunday
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    slot_duration_minutes = Column(Integer, nullable=False, default=15)

    # Relationships
    doctor = relationship("Doctor", back_populates="availability")

class DoctorLeave(Base, TimestampMixin):
    __tablename__ = "doctor_leaves"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    doctor_id = Column(GUID, ForeignKey("doctors.id", ondelete="CASCADE"), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)

    # Relationships
    doctor = relationship("Doctor", back_populates="leaves")
