from __future__ import annotations

from sap_ops_mcp.services.job_service import JobService


def get_failed_jobs(limit: int = 50) -> list[dict]:
    service = JobService()
    return service.get_failed_jobs(limit=limit)


def get_recent_jobs(limit: int = 50) -> list[dict]:
    service = JobService()
    return service.get_recent_jobs(limit=limit)


def get_jobs_by_user(user: str, limit: int = 50) -> list[dict]:
    service = JobService()
    return service.get_jobs_by_user(user=user, limit=limit)


def get_long_running_jobs(threshold_minutes: int = 30, limit: int = 50) -> list[dict]:
    service = JobService()
    return service.get_long_running_jobs(threshold_minutes=threshold_minutes, limit=limit)
