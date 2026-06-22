from contextvars import ContextVar
from typing import Optional
from fastapi import Header, HTTPException, status
from pydantic import UUID4

# Context variable to hold the tenant ID (clinic_id) for the duration of a request
_tenant_context: ContextVar[Optional[UUID4]] = ContextVar("tenant_context", default=None)

def get_tenant_id() -> Optional[UUID4]:
    """Retrieve the current tenant ID from context."""
    return _tenant_context.get()

def set_tenant_id(tenant_id: Optional[UUID4]) -> None:
    """Set the tenant ID in the context."""
    _tenant_context.set(tenant_id)

async def tenant_detector(
    x_clinic_id: Optional[str] = Header(None, alias="X-Clinic-Id")
) -> Optional[UUID4]:
    """
    FastAPI dependency to extract the clinic (tenant) ID from custom headers.
    Ensures that a tenant identifier is present for multi-tenant requests.
    """
    if not x_clinic_id:
        return None
    try:
        from uuid import UUID
        tenant_uuid = UUID(x_clinic_id)
        set_tenant_id(tenant_uuid)
        return tenant_uuid
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Clinic-Id header format. Must be a valid UUID."
        )
