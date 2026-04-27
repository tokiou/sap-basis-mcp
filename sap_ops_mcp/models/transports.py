from __future__ import annotations

from pydantic import BaseModel


class TransportItem(BaseModel):
    transport_id: str
    status: str
    user: str | None = None
    created_at: str | None = None
