from datetime import datetime, date, time
from typing import Optional, List, Any, Dict
from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, UUID4

# -------------------------------------------------------------
# Base Configuration for ORM mapping
# -------------------------------------------------------------
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True

# -------------------------------------------------------------
# Subscription Plan Schemas
# -------------------------------------------------------------
class SubscriptionPlanBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None
    max_doctors: int = Field(..., ge=1)
    max_patients: int = Field(..., ge=1)
    price_monthly: Decimal = Field(..., ge=0.0)
    features: Optional[Dict[str, Any]] = None

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlanUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None
    max_doctors: Optional[int] = Field(None, ge=1)
    max_patients: Optional[int] = Field(None, ge=1)
    price_monthly: Optional[Decimal] = Field(None, ge=0.0)
    features: Optional[Dict[str, Any]] = None

class SubscriptionPlanResponse(SubscriptionPlanBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

# -------------------------------------------------------------
# Clinic Schemas
# -------------------------------------------------------------
class ClinicBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=200)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?[1-9]\d{1,14}$")
    address_line_1: Optional[str] = Field(None, max_length=500)
    address_line_2: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, pattern=r"^\d{5,10}$")
    gstin: Optional[str] = Field(None, pattern=r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$")
    timezone: Optional[str] = Field("UTC", max_length=50)
    logo_url: Optional[str] = None
    subscription_plan_id: Optional[UUID4] = None
    trial_starts_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    is_active: bool = True

class ClinicCreate(ClinicBase):
    pass

class ClinicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=200)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    address_line_1: Optional[str] = Field(None, max_length=500)
    address_line_2: Optional[str] = Field(None, max_length=500)
    city: Optional[str] = Field(None, max_length=100)
    state: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    pincode: Optional[str] = Field(None, pattern=r"^\d{5,10}$")
    gstin: Optional[str] = Field(None, pattern=r"^\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1}$")
    timezone: Optional[str] = Field(None, max_length=50)
    logo_url: Optional[str] = None
    subscription_plan_id: Optional[UUID4] = None
    trial_starts_at: Optional[datetime] = None
    trial_ends_at: Optional[datetime] = None
    is_active: Optional[bool] = None

class ClinicResponse(ClinicBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# Clinic Working Hours Schemas
# -------------------------------------------------------------
class ClinicWorkingHoursBase(BaseSchema):
    clinic_id: UUID4
    day_of_week: int = Field(..., ge=0, le=6)  # 0=Monday, 6=Sunday
    open_time: time
    close_time: time

class ClinicWorkingHoursCreate(ClinicWorkingHoursBase):
    pass

class ClinicWorkingHoursUpdate(BaseModel):
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    open_time: Optional[time] = None
    close_time: Optional[time] = None

class ClinicWorkingHoursResponse(ClinicWorkingHoursBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

# -------------------------------------------------------------
# Department Schemas
# -------------------------------------------------------------
class DepartmentBase(BaseSchema):
    clinic_id: UUID4
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# Role and Permission Schemas
# -------------------------------------------------------------
class PermissionBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class PermissionResponse(PermissionBase):
    id: UUID4
    created_at: datetime

class RoleBase(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = None

class RoleCreate(RoleBase):
    permission_ids: Optional[List[UUID4]] = []

class RoleResponse(RoleBase):
    id: UUID4
    created_at: datetime
    permissions: List[PermissionResponse] = []

# -------------------------------------------------------------
# User Schemas
# -------------------------------------------------------------
class UserBase(BaseSchema):
    clinic_id: UUID4
    role_id: Optional[UUID4] = None
    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    mfa_enabled: bool = False
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserUpdate(BaseModel):
    role_id: Optional[UUID4] = None
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    password: Optional[str] = Field(None, min_length=8, max_length=100)
    mfa_enabled: Optional[bool] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: UUID4
    last_login_at: Optional[datetime] = None
    created_by_id: Optional[UUID4] = Field(None, alias="created_by")
    updated_by_id: Optional[UUID4] = Field(None, alias="updated_by")
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# User MFA Schemas
# -------------------------------------------------------------
class UserMFABase(BaseSchema):
    user_id: UUID4
    secret: str
    backup_codes: Optional[List[str]] = None

class UserMFAResponse(UserMFABase):
    id: UUID4
    verified_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

# -------------------------------------------------------------
# Staff Invitation Schemas
# -------------------------------------------------------------
class StaffInvitationCreate(BaseSchema):
    clinic_id: UUID4
    role_id: Optional[UUID4] = None
    email: EmailStr

class StaffInvitationResponse(BaseSchema):
    id: UUID4
    clinic_id: UUID4
    role_id: Optional[UUID4] = None
    email: EmailStr
    invite_token: str
    status: str
    expires_at: datetime
    created_at: datetime

# -------------------------------------------------------------
# Session and Token Schemas
# -------------------------------------------------------------
class RefreshTokenResponse(BaseSchema):
    id: UUID4
    user_id: UUID4
    token_hash: str
    expires_at: datetime
    revoked_at: Optional[datetime] = None
    created_at: datetime

class UserSessionResponse(BaseSchema):
    id: UUID4
    user_id: UUID4
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    last_activity_at: datetime
    expires_at: datetime
    created_at: datetime

# -------------------------------------------------------------
# Doctor Schemas
# -------------------------------------------------------------
class DoctorBase(BaseSchema):
    clinic_id: UUID4
    user_id: UUID4
    department_id: Optional[UUID4] = None
    specialization: Optional[str] = Field(None, max_length=150)
    qualification: Optional[str] = Field(None, max_length=150)
    registration_number: str = Field(..., min_length=2, max_length=100)
    consultation_fee: Decimal = Field(..., ge=0.0)
    experience_years: Optional[int] = Field(None, ge=0)

class DoctorCreate(DoctorBase):
    pass

class DoctorUpdate(BaseModel):
    department_id: Optional[UUID4] = None
    specialization: Optional[str] = Field(None, max_length=150)
    qualification: Optional[str] = Field(None, max_length=150)
    registration_number: Optional[str] = Field(None, min_length=2, max_length=100)
    consultation_fee: Optional[Decimal] = Field(None, ge=0.0)
    experience_years: Optional[int] = Field(None, ge=0)

class DoctorResponse(DoctorBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# Doctor Availability & Leaves Schemas
# -------------------------------------------------------------
class DoctorAvailabilityBase(BaseSchema):
    doctor_id: UUID4
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: time
    end_time: time
    slot_duration_minutes: int = Field(15, ge=5, le=120)

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    pass

class DoctorAvailabilityResponse(DoctorAvailabilityBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

class DoctorLeaveBase(BaseSchema):
    doctor_id: UUID4
    start_date: date
    end_date: date
    reason: Optional[str] = None

    @model_validator(mode="after")
    def validate_dates(self) -> 'DoctorLeaveBase':
        if self.start_date > self.end_date:
            raise ValueError("start_date cannot be after end_date")
        return self

class DoctorLeaveCreate(DoctorLeaveBase):
    pass

class DoctorLeaveResponse(DoctorLeaveBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

# -------------------------------------------------------------
# Patient Schemas
# -------------------------------------------------------------
class PatientBase(BaseSchema):
    primary_clinic_id: Optional[UUID4] = None
    name: str = Field(..., min_length=2, max_length=150)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=50)
    blood_group: Optional[str] = Field(None, max_length=10)
    address: Optional[str] = Field(None, max_length=500)
    emergency_contact_name: Optional[str] = Field(None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    abha_id: Optional[str] = Field(None, pattern=r"^\d{14}$")  # ABHA is typically 14 digits
    qr_code: Optional[str] = None
    is_minor: bool = False

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    primary_clinic_id: Optional[UUID4] = None
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    email: Optional[EmailStr] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = Field(None, max_length=50)
    blood_group: Optional[str] = Field(None, max_length=10)
    address: Optional[str] = Field(None, max_length=500)
    emergency_contact_name: Optional[str] = Field(None, max_length=150)
    emergency_contact_phone: Optional[str] = Field(None, pattern=r"^\+?[1-9]\d{1,14}$")
    abha_id: Optional[str] = Field(None, pattern=r"^\d{14}$")
    qr_code: Optional[str] = None
    is_minor: Optional[bool] = None

class PatientResponse(PatientBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# Clinic Patient & Guardian Consent Schemas
# -------------------------------------------------------------
class ClinicPatientBase(BaseSchema):
    clinic_id: UUID4
    patient_id: UUID4
    status: str = Field("active", max_length=50)
    linked_at: datetime
    revoked_at: Optional[datetime] = None

class GuardianConsentBase(BaseSchema):
    minor_patient_id: UUID4
    guardian_patient_id: UUID4
    consent_type: str = Field(..., max_length=100)

class GuardianConsentCreate(GuardianConsentBase):
    pass

class GuardianConsentResponse(GuardianConsentBase):
    id: UUID4
    granted_at: datetime
    revoked_at: Optional[datetime] = None

# -------------------------------------------------------------
# Notification Preference Schemas
# -------------------------------------------------------------
class NotificationPreferenceBase(BaseSchema):
    patient_id: UUID4
    email_opt_in: bool = True
    sms_opt_in: bool = True
    whatsapp_opt_in: bool = True
    marketing_opt_in: bool = False

class NotificationPreferenceUpdate(BaseModel):
    email_opt_in: Optional[bool] = None
    sms_opt_in: Optional[bool] = None
    whatsapp_opt_in: Optional[bool] = None
    marketing_opt_in: Optional[bool] = None

class NotificationPreferenceResponse(NotificationPreferenceBase):
    id: UUID4
    created_at: datetime
    updated_at: datetime

# -------------------------------------------------------------
# Appointment Schemas
# -------------------------------------------------------------
class AppointmentBase(BaseSchema):
    clinic_id: UUID4
    doctor_id: UUID4
    patient_id: UUID4
    slot_start: datetime
    slot_end: datetime
    token_number: Optional[int] = None
    queue_position: Optional[int] = None
    checked_in_at: Optional[datetime] = None
    called_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    idempotency_key: Optional[str] = None
    status: str = Field("scheduled", max_length=50)
    notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_slot_times(self) -> 'AppointmentBase':
        if self.slot_start >= self.slot_end:
            raise ValueError("slot_start cannot be after or equal to slot_end")
        return self

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseModel):
    doctor_id: Optional[UUID4] = None
    slot_start: Optional[datetime] = None
    slot_end: Optional[datetime] = None
    token_number: Optional[int] = None
    queue_position: Optional[int] = None
    checked_in_at: Optional[datetime] = None
    called_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: UUID4
    created_by_id: Optional[UUID4] = Field(None, alias="created_by")
    updated_by_id: Optional[UUID4] = Field(None, alias="updated_by")
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

# -------------------------------------------------------------
# Audit Log Schemas
# -------------------------------------------------------------
class AuditLogResponse(BaseSchema):
    id: UUID4
    clinic_id: UUID4
    actor_user_id: Optional[UUID4] = None
    action: str
    entity_type: str
    entity_id: Optional[UUID4] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: datetime
