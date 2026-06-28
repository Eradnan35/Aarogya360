import os
from collections.abc import AsyncGenerator

from sqlalchemy import create_engine, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import ORMExecuteState, Session, sessionmaker

from backend.app.core.config import get_settings
from backend.app.core.tenant import get_tenant_id

settings = get_settings()
DATABASE_URL = os.getenv("DATABASE_URL", settings.database_url)

connect_args: dict = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

# Sync engine (legacy tests / init scripts)
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Async engine (application runtime)
async_engine = create_async_engine(
    settings.async_database_url,
    connect_args=connect_args,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def _enforce_tenant_scoping(execute_state: ORMExecuteState) -> None:
    tenant_id = get_tenant_id()
    if not tenant_id:
        return

    if execute_state.execution_options.get("ignore_tenant", False):
        return

    if execute_state.is_select:
        for desc in execute_state.statement.column_descriptions:
            entity = desc.get("entity")
            if entity and hasattr(entity, "clinic_id"):
                execute_state.statement = execute_state.statement.where(
                    entity.clinic_id == tenant_id
                )
    elif execute_state.is_update or execute_state.is_delete:
        mapper = execute_state.bind_arguments.get("mapper")
        if mapper and hasattr(mapper.class_, "clinic_id"):
            execute_state.statement = execute_state.statement.where(
                mapper.class_.clinic_id == tenant_id
            )


@event.listens_for(Session, "do_orm_execute")
def _sync_enforce_tenant_scoping(execute_state: ORMExecuteState) -> None:
    _enforce_tenant_scoping(execute_state)


@event.listens_for(AsyncSession.sync_session_class, "do_orm_execute")
def _async_enforce_tenant_scoping(execute_state: ORMExecuteState) -> None:
    _enforce_tenant_scoping(execute_state)


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
