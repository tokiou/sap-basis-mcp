from __future__ import annotations

from datetime import datetime

from sap_ops_mcp.models.dumps import DumpItem
from sap_ops_mcp.services.table_reader import TableReaderService


_DUMP_FIELDS = ["UNAME", "DATUM", "UZEIT", "AHOST"]


class DumpService:
    def __init__(self, table_reader: TableReaderService | None = None) -> None:
        self.table_reader = table_reader or TableReaderService()

    def get_recent_dumps(self, limit: int = 50) -> list[dict]:
        rows = self._read_dump_rows(options=[], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def get_dumps_by_user(self, user: str, limit: int = 50) -> list[dict]:
        rows = self._read_dump_rows(options=[f"UNAME = '{user}'"], rowcount=limit)
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def list_dumps(self, rowcount: int = 50) -> list[dict]:
        return self.get_recent_dumps(limit=rowcount)

    def _read_dump_rows(self, options: list[str], rowcount: int) -> list[dict]:
        try:
            return self.table_reader.read_table(
                table="SNAP",
                fields=_DUMP_FIELDS,
                options=options,
                rowcount=rowcount,
            )
        except Exception as exc:
            if "TABLE_NOT_AVAILABLE" not in str(exc):
                raise
            return self.table_reader.read_table(
                table="SNAP_BEG",
                fields=_DUMP_FIELDS,
                options=options,
                rowcount=rowcount,
            )

    def _normalize_row(self, row: dict) -> dict:
        date_value = (row.get("DATUM") or "").strip()
        time_value = (row.get("UZEIT") or "").strip()
        parsed = self._parse_timestamp(date_value, time_value)

        item = DumpItem(
            user=(row.get("UNAME") or "").strip() or None,
            date=parsed.date().isoformat() if parsed else None,
            time=parsed.time().isoformat() if parsed else None,
            host=(row.get("AHOST") or "").strip() or None,
            timestamp=parsed.isoformat(timespec="seconds") if parsed else None,
        )
        return item.model_dump()

    def _parse_timestamp(self, date_value: str, time_value: str) -> datetime | None:
        if len(date_value) != 8 or len(time_value) != 6:
            return None
        try:
            return datetime.strptime(f"{date_value}{time_value}", "%Y%m%d%H%M%S")
        except ValueError:
            return None

    def _sort_key(self, row: dict) -> tuple[int, str]:
        timestamp = row.get("timestamp")
        if not timestamp:
            return (0, "")
        return (1, timestamp)
