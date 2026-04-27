from __future__ import annotations

from datetime import datetime


def parse_date_yyyymmdd(value: str) -> datetime:
    return datetime.strptime(value, "%Y%m%d")
