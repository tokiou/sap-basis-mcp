from __future__ import annotations

from datetime import datetime

from sap_ops_mcp.models.transports import TransportItem
from sap_ops_mcp.services.table_reader import TableReaderService


_TRANSPORT_FIELDS = ["TRKORR", "TRSTATUS", "AS4USER", "AS4DATE", "AS4TIME"]
_TRANSPORT_STATUS_LABELS = {
    "D": "MODIFIABLE",
    "L": "RELEASED",
    "R": "IMPORTED",
}


class TransportService:
    def __init__(self, table_reader: TableReaderService | None = None) -> None:
        self.table_reader = table_reader or TableReaderService()

    def get_recent_transports(self, limit: int = 50) -> list[dict]:
        rows = self.table_reader.read_table(
            table="E070",
            fields=_TRANSPORT_FIELDS,
            options=[],
            rowcount=limit,
        )
        normalized = [self._normalize_row(row) for row in rows]
        return sorted(normalized, key=self._sort_key, reverse=True)[:limit]

    def get_transport_status(self, transport_id: str) -> dict | None:
        options = [f"TRKORR = '{transport_id}'"]
        rows = self.table_reader.read_table(
            table="E070",
            fields=_TRANSPORT_FIELDS,
            options=options,
            rowcount=1,
        )
        if not rows:
            return None

        row = rows[0]
        status_code = (row.get("TRSTATUS") or "").strip()

        try:
            detail_rows = self.table_reader.read_table(
                table="E070A",
                fields=["TRKORR", "TRSTATUS"],
                options=options,
                rowcount=1,
            )
            if detail_rows:
                detailed_status = (detail_rows[0].get("TRSTATUS") or "").strip()
                if detailed_status:
                    status_code = detailed_status
        except Exception:
            pass

        row["TRSTATUS"] = status_code
        return self._normalize_row(row)

    def get_failed_transports(self, limit: int = 50) -> list[dict]:
        rows = self.table_reader.read_table(
            table="E070",
            fields=_TRANSPORT_FIELDS,
            options=["TRSTATUS <> 'R' AND TRSTATUS <> 'L' AND TRSTATUS <> 'D'"],
            rowcount=limit,
        )
        return [self._normalize_row(row, failed_context=True) for row in rows]

    def _normalize_row(self, row: dict, failed_context: bool = False) -> dict:
        created_dt = self._parse_created_datetime(
            date_value=(row.get("AS4DATE") or "").strip(),
            time_value=(row.get("AS4TIME") or "").strip(),
        )
        item = TransportItem(
            transport_id=(row.get("TRKORR") or "").strip(),
            status=self._map_status((row.get("TRSTATUS") or "").strip(), failed_context=failed_context),
            user=(row.get("AS4USER") or "").strip() or None,
            created_at=created_dt.isoformat(timespec="seconds") if created_dt else None,
        )
        return item.model_dump()

    def _map_status(self, status_code: str, failed_context: bool = False) -> str:
        if not status_code:
            return "UNKNOWN"
        if status_code in _TRANSPORT_STATUS_LABELS:
            return _TRANSPORT_STATUS_LABELS[status_code]
        if failed_context:
            return "FAILED"
        return status_code

    def _parse_created_datetime(self, date_value: str, time_value: str) -> datetime | None:
        if len(date_value) != 8 or len(time_value) != 6:
            return None
        try:
            return datetime.strptime(f"{date_value}{time_value}", "%Y%m%d%H%M%S")
        except ValueError:
            return None

    def _sort_key(self, row: dict) -> tuple[int, str]:
        created_at = row.get("created_at")
        if not created_at:
            return (0, "")
        return (1, created_at)
