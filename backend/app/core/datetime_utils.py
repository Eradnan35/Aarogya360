from datetime import UTC, datetime


def utc_now() -> datetime:
    """Return naive UTC datetime compatible with existing TIMESTAMP columns."""
    return datetime.now(UTC).replace(tzinfo=None)
