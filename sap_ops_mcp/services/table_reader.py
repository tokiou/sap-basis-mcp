from __future__ import annotations

from typing import Any

from sap_ops_mcp.clients.rfc import SAPRFCClient


class TableReaderService:
    def __init__(self, client: SAPRFCClient | None = None) -> None:
        self.client = client or SAPRFCClient()

    def read_table(
        self,
        table: str,
        fields: list[str] | None = None,
        options: list[str] | None = None,
        rowcount: int = 100,
    ) -> list[dict[str, Any]]:
        field_defs = [{"FIELDNAME": f} for f in (fields or [])]
        option_defs = [{"TEXT": o} for o in (options or [])]

        response = self.client.call(
            "RFC_READ_TABLE",
            QUERY_TABLE=table,
            DELIMITER="|",
            FIELDS=field_defs,
            OPTIONS=option_defs,
            ROWCOUNT=rowcount,
        )

        rows = response.get("DATA", [])
        keys = fields or []
        parsed: list[dict[str, Any]] = []

        for row in rows:
            raw = row.get("WA", "")
            values = raw.split("|")
            parsed.append({k: values[idx] if idx < len(values) else None for idx, k in enumerate(keys)})

        return parsed
