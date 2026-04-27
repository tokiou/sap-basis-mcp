from __future__ import annotations

from sap_ops_mcp.services.transport_service import TransportService


def get_recent_transports(limit: int = 50) -> list[dict]:
    service = TransportService()
    return service.get_recent_transports(limit=limit)


def get_transport_status(transport_id: str) -> dict | None:
    service = TransportService()
    return service.get_transport_status(transport_id=transport_id)


def get_failed_transports(limit: int = 50) -> list[dict]:
    service = TransportService()
    return service.get_failed_transports(limit=limit)


def get_transports(rowcount: int = 100) -> list[dict]:
    return get_recent_transports(limit=rowcount)
