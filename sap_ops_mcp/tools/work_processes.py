from __future__ import annotations

from sap_ops_mcp.services.work_process_service import WorkProcessService


def get_work_processes() -> list[dict]:
    service = WorkProcessService()
    return service.get_work_processes()


def get_running_work_processes() -> list[dict]:
    service = WorkProcessService()
    return service.get_running_work_processes()


def get_work_processes_by_type(process_type: str) -> list[dict]:
    service = WorkProcessService()
    return service.get_work_processes_by_type(process_type=process_type)
