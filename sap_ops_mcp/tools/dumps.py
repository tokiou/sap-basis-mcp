from __future__ import annotations

from sap_ops_mcp.services.dump_service import DumpService


def get_recent_dumps(limit: int = 50) -> list[dict]:
    service = DumpService()
    return service.get_recent_dumps(limit=limit)


def get_dumps_by_user(user: str, limit: int = 50) -> list[dict]:
    service = DumpService()
    return service.get_dumps_by_user(user=user, limit=limit)


def get_dumps(rowcount: int = 50) -> list[dict]:
    return get_recent_dumps(limit=rowcount)
