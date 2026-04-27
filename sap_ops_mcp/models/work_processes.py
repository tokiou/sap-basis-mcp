from __future__ import annotations

from pydantic import BaseModel


class WorkProcessItem(BaseModel):
    wp_no: int | str | None = None
    type: str | None = None
    status: str | None = None
    user: str | None = None
    program: str | None = None
