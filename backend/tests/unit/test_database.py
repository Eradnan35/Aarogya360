import pytest
from datetime import datetime, date, time, timedelta
from decimal import Decimal
from uuid import uuid4
from pydantic import ValidationError
from sqlalchemy import select

from backend.database.database import engine
from backend.database.models.base import Base
from backend.database.models.clinic import Clinic, SubscriptionPlan, Department
from backend.database.models.user import User, Role
from backend.database.models.patient import Patient
from backend.database.models.appointment import Appointment
from backend.database.database import SessionLocal
from backend.app.core.tenant import set_tenant_id, get_tenant_id
from backend.database.schemas import ClinicCreate, UserCreate, DoctorLeaveCreate, AppointmentCreate
import backend.database.session  # Register event hooks


@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # Create the tables in SQLite for testing
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    session = SessionLocal()
    # Reset tenant context before each test
    set_tenant_id(None)
    try:
        yield session
    finally:
        session.close()

def test_tenant_isolation(db_session):
    # 1. Create two clinics (tenants)
    clinic_a_id = uuid4()
    clinic_b_id = uuid4()

    clinic_a = Clinic(
        id=clinic_a_id,
        name="Clinic A",
        email="clinica@example.com",
        phone="+1234567890",
        is_active=True
    )
    clinic_b = Clinic(
        id=clinic_b_id,
        name="Clinic B",
        email="clinicb@example.com",
        phone="+1987654321",
        is_active=True
    )
    db_session.add_all([clinic_a, clinic_b])
    db_session.commit()

    # 2. Add departments to both clinics
    dept_a = Department(id=uuid4(), clinic_id=clinic_a_id, name="Cardiology")
    dept_b = Department(id=uuid4(), clinic_id=clinic_b_id, name="Pediatrics")
    db_session.add_all([dept_a, dept_b])
    db_session.commit()

    # 3. Query without tenant context (should return both departments)
    set_tenant_id(None)
    all_depts = db_session.execute(select(Department)).scalars().all()
    assert len(all_depts) >= 2

    # 4. Set tenant context to Clinic A
    set_tenant_id(clinic_a_id)
    depts_a = db_session.execute(select(Department)).scalars().all()
    assert len(depts_a) == 1
    assert depts_a[0].name == "Cardiology"

    # 5. Set tenant context to Clinic B
    set_tenant_id(clinic_b_id)
    depts_b = db_session.execute(select(Department)).scalars().all()
    assert len(depts_b) == 1
    assert depts_b[0].name == "Pediatrics"

    # Clean up
    set_tenant_id(None)


def test_pydantic_schema_validation():
    # Valid clinic validation
    valid_clinic = ClinicCreate(
        name="Healthy Clinic",
        email="info@healthy.com",
        phone="+919876543210",
        gstin="27AAAAA1111A1Z1"  # Matches standard GSTIN format
    )
    assert valid_clinic.name == "Healthy Clinic"

    # Invalid email validation
    with pytest.raises(ValidationError):
        ClinicCreate(
            name="Healthy Clinic",
            email="not-an-email",
            phone="+919876543210"
        )

    # Invalid phone validation
    with pytest.raises(ValidationError):
        ClinicCreate(
            name="Healthy Clinic",
            email="info@healthy.com",
            phone="invalid-phone-123"
        )

    # Invalid doctor leave dates (start after end)
    with pytest.raises(ValidationError):
        DoctorLeaveCreate(
            doctor_id=uuid4(),
            start_date=date(2026, 6, 25),
            end_date=date(2026, 6, 20),
            reason="Vacation"
        )


def test_sql_injection_prevention(db_session):
    # Test that parameters are treated as literal strings and do not cause injection
    clinic_id = uuid4()
    malicious_name = "Clinic A'; DROP TABLE clinics; --"
    
    clinic = Clinic(
        id=clinic_id,
        name=malicious_name,
        email="injection@test.com",
        phone="+15555555555"
    )
    db_session.add(clinic)
    db_session.commit()
    
    # Query using SQLAlchemy's parameterized queries
    queried_clinic = db_session.execute(
        select(Clinic).where(Clinic.name == malicious_name)
    ).scalar_one_or_none()
    
    assert queried_clinic is not None
    assert queried_clinic.id == clinic_id
    
    # Verify the table was NOT dropped and data is safe
    all_clinics = db_session.execute(select(Clinic)).scalars().all()
    assert len(all_clinics) > 0
