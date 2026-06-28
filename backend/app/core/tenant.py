from contextvars import ContextVar
from typing import Optional
from uuid import UUID

from fastapi import Header, HTTPException, status

_tenant_context: ContextVar[Optional[UUID]] = ContextVar("tenant_context", default=None)


def get_tenant_id() -> Optional[UUID]:
    return _tenant_context.get()


def set_tenant_id(tenant_id: Optional[UUID]) -> None:
    _tenant_context.set(tenant_id)


def clear_tenant_id() -> None:
    _tenant_context.set(None)


async def tenant_detector(
    x_clinic_id: Optional[str] = Header(None, alias="X-Clinic-Id"),
) -> Optional[UUID]:
    """Extract clinic ID from header (fallback when JWT tenant is not yet set)."""
    if not x_clinic_id:
        return get_tenant_id()
    try:
        tenant_uuid = UUID(x_clinic_id)
        set_tenant_id(tenant_uuid)
        return tenant_uuid
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-Clinic-Id header format. Must be a valid UUID.",
        ) from exc


def set_tenant_from_jwt(clinic_id: UUID) -> None:
    """Set tenant context from validated JWT claims."""
    set_tenant_id(clinic_id)
