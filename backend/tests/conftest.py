import os

import pytest

# ---------------------------------------------------------------------------
# CRITICAL: Use a separate test database so pytest never drops dev/prod tables.
# Must run BEFORE any backend.database import.
# ---------------------------------------------------------------------------
os.environ.setdefault(
    "TEST_DATABASE_URL",
    "postgresql://postgres:admin123@localhost/Aarogya360_test",
)
os.environ["DATABASE_URL"] = os.environ["TEST_DATABASE_URL"]

os.environ.setdefault("SECRET_KEY", "test-secret-key-minimum-32-characters-long")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")

from backend.app.core.config import get_settings

get_settings.cache_clear()


@pytest.fixture(scope="session", autouse=True)
def ensure_test_database():
    """Create isolated test database and tables once per test session."""
    from backend.database.database import DATABASE_URL, engine
    from backend.database.db_utils import ensure_database_exists
    from backend.database.models.base import Base
    import backend.database.models  # noqa: F401

    ensure_database_exists(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    # Only drop tables on the TEST database — never on Aarogya360 dev DB
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
async def dispose_async_connections():
    """Prevent asyncpg pool connections from leaking across event loops (Windows)."""
    yield
    from backend.database.database import async_engine

    await async_engine.dispose()
