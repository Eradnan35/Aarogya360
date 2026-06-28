"""Database utility helpers for initialization and diagnostics."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine


def parse_database_url(url: str) -> dict[str, Any]:
    """Parse a SQLAlchemy PostgreSQL URL into connection components."""
    normalized = url.replace("postgresql+asyncpg://", "postgresql://").replace(
        "postgresql+psycopg2://", "postgresql://"
    )
    parsed = urlparse(normalized)
    database = parsed.path.lstrip("/") if parsed.path else ""
    return {
        "host": parsed.hostname or "localhost",
        "port": parsed.port or 5432,
        "user": parsed.username or "postgres",
        "password": parsed.password or "",
        "database": database,
        "url": url,
    }


def build_admin_url(url: str) -> str:
    """Build a connection URL to the default `postgres` maintenance database."""
    info = parse_database_url(url)
    password = info["password"]
    auth = f"{info['user']}:{password}" if password else info["user"]
    return f"postgresql://{auth}@{info['host']}:{info['port']}/postgres"


def ensure_database_exists(database_url: str) -> None:
    """Create the target PostgreSQL database if it does not exist."""
    info = parse_database_url(database_url)
    db_name = info["database"]
    if not db_name:
        raise ValueError("DATABASE_URL must include a database name")

    admin_engine = create_engine(build_admin_url(database_url), isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": db_name},
            ).fetchone()
            if exists:
                return

            # Quote identifier to preserve case (e.g. Aarogya360)
            if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", db_name):
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            else:
                conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Created database: {db_name}")
    finally:
        admin_engine.dispose()


def list_public_tables(engine: Engine) -> list[str]:
    return sorted(inspect(engine).get_table_names(schema="public"))


def print_connection_report(engine: Engine, database_url: str) -> None:
    info = parse_database_url(database_url)
    print("\n--- PostgreSQL connection ---")
    print(f"  Host     : {info['host']}")
    print(f"  Port     : {info['port']}")
    print(f"  User     : {info['user']}")
    print(f"  Database : {info['database']}")
    print("  Schema   : public")
    print("\nIn pgAdmin: connect to this exact database name, then open")
    print("  Schemas -> public -> Tables  (right-click -> Refresh)")
    print("-----------------------------\n")

    with engine.connect() as conn:
        row = conn.execute(text("SELECT current_database(), current_schema()")).fetchone()
        print(f"Connected to database: {row[0]} | schema: {row[1]}")

    tables = list_public_tables(engine)
    print(f"\nTables found in public schema: {len(tables)}")
    for name in tables:
        print(f"  - {name}")

    if not tables:
        print("\nWARNING: No tables in public schema.")
        print("Run: python -m backend.database.init_db")
