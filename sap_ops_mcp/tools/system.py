from __future__ import annotations

from sap_ops_mcp.settings import get_settings


def system_info() -> dict[str, str]:
    settings = get_settings()
    return {
        "app_name": settings.app_name,
        "app_env": settings.app_env,
        "sap_host": settings.sap_ashost,
        "sap_client": settings.sap_client,
    }
