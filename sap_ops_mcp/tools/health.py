from __future__ import annotations

from sap_ops_mcp.services.health_service import HealthService


def health_check() -> dict[str, str]:
    service = HealthService()
    return service.check()
