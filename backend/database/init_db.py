"""
Initialize PostgreSQL tables for Aarogya360.

Usage (from project root):
    python -m backend.database.init_db

Optional:
    python -m backend.database.init_db --verify   # only check connection + list tables
    python -m backend.database.init_db --create-db  # create DB if missing, then create tables
"""

from __future__ import annotations

import argparse
import os
import sys

# Ensure project root is on sys.path when run as a script
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.database.database import DATABASE_URL, engine  # noqa: E402
from backend.database.db_utils import (  # noqa: E402
    ensure_database_exists,
    list_public_tables,
    print_connection_report,
)
from backend.database.models.base import Base  # noqa: E402
import backend.database.models  # noqa: F401, E402 — register all models on Base.metadata

EXPECTED_TABLE_COUNT = 21


def init_db(*, create_database: bool = False) -> int:
    print("Initializing Aarogya360 database tables...")
    print(f"DATABASE_URL={DATABASE_URL}")

    if create_database:
        ensure_database_exists(DATABASE_URL)

    print_connection_report(engine, DATABASE_URL)

    registered = sorted(Base.metadata.tables.keys())
    print(f"\nModels registered in SQLAlchemy metadata: {len(registered)}")
    for name in registered:
        print(f"  - {name}")

    existing_before = set(list_public_tables(engine))
    Base.metadata.create_all(bind=engine)
    existing_after = set(list_public_tables(engine))
    created = existing_after - existing_before

    if created:
        print(f"\nNewly created tables: {len(created)}")
        for name in sorted(created):
            print(f"  + {name}")
    else:
        print("\nNo new tables needed (all already exist).")

    final_tables = list_public_tables(engine)
    print(f"\nTotal tables in database: {len(final_tables)}")

    if len(final_tables) < EXPECTED_TABLE_COUNT:
        print(
            f"\nWARNING: Expected at least {EXPECTED_TABLE_COUNT} tables, "
            f"found {len(final_tables)}.",
            file=sys.stderr,
        )
        return 1

    print("\nSuccess: database is ready.")
    return 0


def verify_db() -> int:
    print(f"Verifying database: {DATABASE_URL}")
    print_connection_report(engine, DATABASE_URL)
    count = len(list_public_tables(engine))
    if count == 0:
        print("\nNo tables found. Run: python -m backend.database.init_db")
        return 1
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Aarogya360 database initialization")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify connection and list tables without creating anything",
    )
    parser.add_argument(
        "--create-db",
        action="store_true",
        help="Create the PostgreSQL database if it does not exist",
    )
    args = parser.parse_args()

    try:
        code = verify_db() if args.verify else init_db(create_database=args.create_db)
    except Exception as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        print(
            "\nCommon fixes:\n"
            "  1. Ensure PostgreSQL is running\n"
            "  2. Create database in pgAdmin or run with --create-db\n"
            "  3. Set DATABASE_URL in .env to match pgAdmin connection\n"
            "  4. In pgAdmin, select the correct database (not 'postgres')\n"
            "  5. Refresh: Schemas -> public -> Tables",
            file=sys.stderr,
        )
        sys.exit(1)

    sys.exit(code)


if __name__ == "__main__":
    main()
