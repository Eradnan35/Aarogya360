from collections.abc import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from backend.database.database import AsyncSessionLocal, SessionLocal, get_async_db

__all__ = ["get_db", "get_async_db", "SessionLocal", "AsyncSessionLocal"]


def get_db() -> Generator[Session, None, None]:
    """Sync FastAPI dependency (legacy/tests)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async FastAPI dependency with automatic commit/rollback."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
