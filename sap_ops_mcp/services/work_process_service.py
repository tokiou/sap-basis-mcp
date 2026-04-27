from __future__ import annotations

from typing import Any

from sap_ops_mcp.clients.rfc import SAPRFCClient
from sap_ops_mcp.models.work_processes import WorkProcessItem


_TYPE_ALIASES = {
    "BTC": "BGD",
}


class WorkProcessService:
    def __init__(self, client: SAPRFCClient | None = None) -> None:
        self.client = client or SAPRFCClient()

    def get_work_processes(self) -> list[dict]:
        response = self.client.call("TH_WPINFO")
        rows = response.get("WPLIST", [])
        return [self._normalize_row(row) for row in rows]

    def get_running_work_processes(self) -> list[dict]:
        rows = self.get_work_processes()
        return [row for row in rows if (row.get("status") or "").upper() == "RUNNING"]

    def get_work_processes_by_type(self, process_type: str) -> list[dict]:
        target = process_type.strip().upper()
        target = _TYPE_ALIASES.get(target, target)
        rows = self.get_work_processes()
        return [row for row in rows if (row.get("type") or "").upper() == target]

    def _normalize_row(self, row: dict[str, Any]) -> dict:
        wp_no_value = row.get("WP_NO")
        if isinstance(wp_no_value, str):
            stripped = wp_no_value.strip()
            wp_no: int | str | None
            if stripped.isdigit():
                wp_no = int(stripped)
            else:
                wp_no = stripped or None
        elif isinstance(wp_no_value, int):
            wp_no = wp_no_value
        else:
            wp_no = None

        wp_type = (row.get("WP_TYP") or "").strip().upper() or None
        status = (row.get("WP_STATUS") or row.get("WP_ISTATUS") or "").strip()
        user = (row.get("WP_USER") or row.get("WP_BNAME") or "").strip() or None
        program = (row.get("WP_PROGRAM") or row.get("WP_REPORT") or "").strip() or None

        item = WorkProcessItem(
            wp_no=wp_no,
            type=wp_type,
            status=status.upper() if isinstance(status, str) else None,
            user=user,
            program=program,
        )
        return item.model_dump()
