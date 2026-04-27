from __future__ import annotations

from datetime import datetime

from sap_ops_mcp.models.spool import SpoolItem
from sap_ops_mcp.services.table_reader import TableReaderService


_SPOOL_FIELDS = ["RQIDENT", "RQOWNER", "RQCRETIME", "RQSTATUS", "RQDEST"]
_STATUS_MAP = {
    "F": "ERROR",
    "C": "COMPLETED",
    "P": "PROCESSING",
}


class SpoolService:
    def __init__(self, table_reader: TableReaderService | None = None) -> None:
        self.table_reader = table_reader or TableReaderService()

    def get_recent_spool_requests(self, limit: int = 50) -> list[dict]:
        rows = self._read_spool(options=[], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def get_spool_errors(self, limit: int = 50) -> list[dict]:
        rows = self._read_spool(options=["RQSTATUS = 'F'"], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def get_spool_by_user(self, user: str, limit: int = 50) -> list[dict]:
        rows = self._read_spool(options=[f"RQOWNER = '{user}'"], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def _read_spool(self, options: list[str], rowcount: int) -> list[dict]:
        try:
            return self.table_reader.read_table(
                table="TSP01",
                fields=_SPOOL_FIELDS,
                options=options,
                rowcount=rowcount,
            )
        except Exception as exc:
            if "TABLE_WITHOUT_DATA" in str(exc):
                return []
            raise

    def _normalize_row(self, row: dict) -> dict:
        created_at = self._parse_created_at((row.get("RQCRETIME") or "").strip())
        status_code = (row.get("RQSTATUS") or "").strip().upper()
        item = SpoolItem(
            spool_id=(row.get("RQIDENT") or "").strip(),
            user=(row.get("RQOWNER") or "").strip() or None,
            status=_STATUS_MAP.get(status_code, status_code or "UNKNOWN"),
            created_at=created_at.isoformat(timespec="seconds") if created_at else None,
            destination=(row.get("RQDEST") or "").strip() or None,
        )
        return item.model_dump()

    def _parse_created_at(self, value: str) -> datetime | None:
        if len(value) == 14 and value.isdigit():
            try:
                return datetime.strptime(value, "%Y%m%d%H%M%S")
            except ValueError:
                return None
        return None

    def _sort_key(self, item: dict) -> tuple[int, str]:
        created_at = item.get("created_at")
        if not created_at:
            return (0, "")
        return (1, created_at)
