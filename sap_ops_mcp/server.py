from __future__ import annotations

from sap_ops_mcp.services.health_service import HealthService
from sap_ops_mcp.settings import get_settings
from sap_ops_mcp.tools.jobs import (
    get_failed_jobs,
    get_jobs_by_user,
    get_long_running_jobs,
    get_recent_jobs,
)
from sap_ops_mcp.tools.dumps import get_dumps_by_user, get_recent_dumps
from sap_ops_mcp.tools.spool import (
    get_recent_spool_requests,
    get_spool_by_user,
    get_spool_errors,
)
from sap_ops_mcp.tools.transports import (
    get_failed_transports,
    get_recent_transports,
    get_transport_status,
)
from sap_ops_mcp.tools.work_processes import (
    get_running_work_processes,
    get_work_processes,
    get_work_processes_by_type,
)

try:
    from mcp.server.fastmcp import FastMCP  # type: ignore
except Exception:  # pragma: no cover
    FastMCP = None


def build_server() -> object:
    settings = get_settings()
    health_service = HealthService()

    if FastMCP is None:
        return {
            "name": settings.app_name,
            "status": "mcp dependency missing",
            "health": health_service.check(),
        }

    mcp = FastMCP(settings.app_name)

    @mcp.tool()
    def ping() -> dict:
        return health_service.check()

    @mcp.tool()
    def jobs_failed(limit: int = 50) -> list[dict]:
        return get_failed_jobs(limit=limit)

    @mcp.tool()
    def jobs_recent(limit: int = 50) -> list[dict]:
        return get_recent_jobs(limit=limit)

    @mcp.tool()
    def jobs_by_user(user: str, limit: int = 50) -> list[dict]:
        return get_jobs_by_user(user=user, limit=limit)

    @mcp.tool()
    def jobs_long_running(threshold_minutes: int = 30, limit: int = 50) -> list[dict]:
        return get_long_running_jobs(threshold_minutes=threshold_minutes, limit=limit)

    @mcp.tool()
    def transports_recent(limit: int = 50) -> list[dict]:
        return get_recent_transports(limit=limit)

    @mcp.tool()
    def transport_status(transport_id: str) -> dict | None:
        return get_transport_status(transport_id=transport_id)

    @mcp.tool()
    def transports_failed(limit: int = 50) -> list[dict]:
        return get_failed_transports(limit=limit)

    @mcp.tool()
    def dumps_recent(limit: int = 50) -> list[dict]:
        return get_recent_dumps(limit=limit)

    @mcp.tool()
    def dumps_by_user(user: str, limit: int = 50) -> list[dict]:
        return get_dumps_by_user(user=user, limit=limit)

    @mcp.tool()
    def work_processes() -> list[dict]:
        return get_work_processes()

    @mcp.tool()
    def work_processes_running() -> list[dict]:
        return get_running_work_processes()

    @mcp.tool()
    def work_processes_by_type(process_type: str) -> list[dict]:
        return get_work_processes_by_type(process_type=process_type)

    @mcp.tool()
    def spool_recent(limit: int = 50) -> list[dict]:
        return get_recent_spool_requests(limit=limit)

    @mcp.tool()
    def spool_errors(limit: int = 50) -> list[dict]:
        return get_spool_errors(limit=limit)

    @mcp.tool()
    def spool_by_user(user: str, limit: int = 50) -> list[dict]:
        return get_spool_by_user(user=user, limit=limit)

    return mcp


def main() -> None:
    server = build_server()
    if hasattr(server, "run"):
        server.run()  # type: ignore[attr-defined]
    else:
        print(server)


if __name__ == "__main__":
    main()
