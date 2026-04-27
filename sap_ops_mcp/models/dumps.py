from __future__ import annotations

from pydantic import BaseModel


class DumpItem(BaseModel):
    user: str | None = None
    date: str | None = None
    time: str | None = None
    host: str | None = None
    timestamp: str | None = None
