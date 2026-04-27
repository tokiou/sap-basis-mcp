from __future__ import annotations

from sap_ops_mcp.services.spool_service import SpoolService


def get_recent_spool_requests(limit: int = 50) -> list[dict]:
    service = SpoolService()
    return service.get_recent_spool_requests(limit=limit)


def get_spool_errors(limit: int = 50) -> list[dict]:
    service = SpoolService()
    return service.get_spool_errors(limit=limit)


def get_spool_by_user(user: str, limit: int = 50) -> list[dict]:
    service = SpoolService()
    return service.get_spool_by_user(user=user, limit=limit)
