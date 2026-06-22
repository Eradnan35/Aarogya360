from typing import Generator
from sqlalchemy import event
from sqlalchemy.orm import Session, ORMExecuteState
from backend.database.database import SessionLocal
from backend.app.core.tenant import get_tenant_id

# Event listener for SQLAlchemy Session to automatically enforce multi-tenancy scoping
@event.listens_for(Session, "do_orm_execute")
def _enforce_tenant_scoping(execute_state: ORMExecuteState):
    """
    Automatically scopes all SELECT, UPDATE, and DELETE statements to the active clinic_id
    if a tenant context is set and the model contains a 'clinic_id' attribute.
    """
    tenant_id = get_tenant_id()
    if not tenant_id:
        return

    # Check if the execution option explicitly requests to bypass tenancy scoping
    if execute_state.execution_options.get("ignore_tenant", False):
        return

    # Apply scoping based on statement type
    if execute_state.is_select:
        # Re-write the select statement to include tenant filtering
        for desc in execute_state.statement.column_descriptions:
            entity = desc.get("entity")
            if entity and hasattr(entity, "clinic_id"):
                execute_state.statement = execute_state.statement.where(
                    entity.clinic_id == tenant_id
                )
    elif execute_state.is_update or execute_state.is_delete:
        # Re-write the update/delete statement to include tenant filtering
        mapper = execute_state.bind_arguments.get("mapper")
        if mapper and hasattr(mapper.class_, "clinic_id"):
            execute_state.statement = execute_state.statement.where(
                mapper.class_.clinic_id == tenant_id
            )

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency to yield database session.
    Ensures the session is correctly closed after request completion.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
