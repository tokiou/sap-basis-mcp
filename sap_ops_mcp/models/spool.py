from __future__ import annotations

from pydantic import BaseModel


class SpoolItem(BaseModel):
    spool_id: str
    user: str | None = None
    status: str
    created_at: str | None = None
    destination: str | None = None
