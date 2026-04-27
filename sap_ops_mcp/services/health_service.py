from __future__ import annotations

from datetime import datetime, timezone


class HealthService:
    def check(self) -> dict[str, str]:
        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
