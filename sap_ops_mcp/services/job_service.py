from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from sap_ops_mcp.models.jobs import JobItem
from sap_ops_mcp.services.table_reader import TableReaderService


_JOB_FIELDS = ["JOBNAME", "STATUS", "SDLUNAME", "SDLSTRTDT", "SDLSTRTTM"]
_STATUS_LABELS = {
    "A": "ABORTED",
    "F": "FAILED",
    "R": "RUNNING",
    "S": "SCHEDULED",
}


class JobService:
    def __init__(
        self,
        table_reader: TableReaderService | None = None,
        now_provider: Callable[[], datetime] | None = None,
    ) -> None:
        self.table_reader = table_reader or TableReaderService()
        self.now_provider = now_provider or (lambda: datetime.now(timezone.utc))

    def get_failed_jobs(self, limit: int = 50) -> list[dict]:
        rows = self._read_jobs(options=["STATUS = 'A' OR STATUS = 'F'"], rowcount=limit)
        return [self._normalize_row(row) for row in rows]

    def get_recent_jobs(self, limit: int = 50) -> list[dict]:
        rows = self._read_jobs(options=[], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        ordered = sorted(normalized, key=self._sort_key, reverse=True)
        return ordered[:limit]

    def get_jobs_by_user(self, user: str, limit: int = 50) -> list[dict]:
        rows = self._read_jobs(options=[f"SDLUNAME = '{user}'"], rowcount=limit)
        return [self._normalize_row(row) for row in rows]

    def get_long_running_jobs(self, threshold_minutes: int = 30, limit: int = 50) -> list[dict]:
        rows = self._read_jobs(options=["STATUS = 'R'"], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        now = self.now_provider()
        running: list[dict] = []

        for item in normalized:
            started_at = item.get("started_at")
            if not started_at:
                continue
            started_dt = datetime.fromisoformat(started_at).replace(tzinfo=timezone.utc)
            elapsed_minutes = (now - started_dt).total_seconds() / 60
            if elapsed_minutes > threshold_minutes:
                running.append(item)

        return running

    def _read_jobs(self, options: list[str], rowcount: int) -> list[dict]:
        return self.table_reader.read_table(
            table="TBTCO",
            fields=_JOB_FIELDS,
            options=options,
            rowcount=rowcount,
        )

    def _normalize_row(self, row: dict) -> dict:
        started_dt = self._parse_started_datetime(
            start_date=(row.get("SDLSTRTDT") or "").strip(),
            start_time=(row.get("SDLSTRTTM") or "").strip(),
        )

        item = JobItem(
            job_name=(row.get("JOBNAME") or "").strip(),
            status=self._map_status((row.get("STATUS") or "").strip()),
            user=(row.get("SDLUNAME") or "").strip() or None,
            started_at=started_dt.isoformat(timespec="seconds") if started_dt else None,
        )
        return item.model_dump()

    def _map_status(self, status_code: str) -> str:
        if not status_code:
            return "UNKNOWN"
        return _STATUS_LABELS.get(status_code, status_code)

    def _parse_started_datetime(self, start_date: str, start_time: str) -> datetime | None:
        if len(start_date) != 8 or len(start_time) != 6:
            return None
        try:
            parsed = datetime.strptime(f"{start_date}{start_time}", "%Y%m%d%H%M%S")
        except ValueError:
            return None
        return parsed

    def _sort_key(self, row: dict) -> tuple[int, str]:
        started_at = row.get("started_at")
        if not started_at:
            return (0, "")
        return (1, started_at)
