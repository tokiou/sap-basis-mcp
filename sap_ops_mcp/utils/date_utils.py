from __future__ import annotations

from datetime import datetime, timezone


def to_utc_iso(value: datetime | None = None) -> str:
    base = value or datetime.now(timezone.utc)
    if base.tzinfo is None:
        base = base.replace(tzinfo=timezone.utc)
    return base.astimezone(timezone.utc).isoformat()
