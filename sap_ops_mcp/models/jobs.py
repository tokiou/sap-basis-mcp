from __future__ import annotations

from pydantic import BaseModel


class JobFilter(BaseModel):
    status: str | None = None
    user: str | None = None


class JobItem(BaseModel):
    job_name: str
    status: str
    user: str | None = None
    started_at: str | None = None
