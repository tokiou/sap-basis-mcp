from __future__ import annotations

import ctypes
import importlib
import os
from pathlib import Path
from typing import Any

from sap_ops_mcp.clients.errors import SAPConnectionError, SAPRFCError
from sap_ops_mcp.settings import get_settings

try:
    from pyrfc import Connection  # type: ignore
except Exception:  # pragma: no cover
    Connection = None


def _candidate_lib_dirs() -> list[Path]:
    dirs: list[Path] = []
    sapnwrfc_home = os.getenv("SAPNWRFC_HOME", "")
    if sapnwrfc_home:
        dirs.append(Path(sapnwrfc_home) / "lib")
    dirs.append(Path("/opt/nwrfcsdk/lib"))
    dirs.append(Path(__file__).resolve().parents[2] / "nwrfcsdk" / "lib")
    return dirs


def _load_nwrfc_runtime() -> None:
    for lib_dir in _candidate_lib_dirs():
        if not lib_dir.exists():
            continue
        lib_path = lib_dir / "libsapnwrfc.so"
        if lib_path.exists():
            try:
                ctypes.CDLL(str(lib_path), mode=ctypes.RTLD_GLOBAL)
            except Exception:
                continue


def _resolve_connection_class() -> Any | None:
    global Connection
    if Connection is not None:
        return Connection

    try:
        import pyrfc  # type: ignore

        connection_cls = getattr(pyrfc, "Connection", None)
        if connection_cls is not None:
            Connection = connection_cls
            return Connection
    except Exception:
        pass

    _load_nwrfc_runtime()

    try:
        pyrfc_module = importlib.import_module("pyrfc")
        pyrfc_module = importlib.reload(pyrfc_module)
        connection_cls = getattr(pyrfc_module, "Connection", None)
        if connection_cls is not None:
            Connection = connection_cls
            return Connection
    except Exception:
        return None

    return None


class SAPRFCClient:
    def __init__(self) -> None:
        self._settings = get_settings()
        self._conn: Any | None = None

    def connect(self) -> None:
        connection_cls = _resolve_connection_class()
        if connection_cls is None:
            raise SAPConnectionError("PyRFC no esta disponible en el entorno")

        try:
            self._conn = connection_cls(
                ashost=self._settings.sap_ashost,
                sysnr=self._settings.sap_sysnr,
                client=self._settings.sap_client,
                user=self._settings.sap_user,
                passwd=self._settings.sap_passwd,
                lang=self._settings.sap_lang,
            )
        except Exception as exc:  # pragma: no cover
            raise SAPConnectionError(str(exc)) from exc

    def call(self, func_name: str, **kwargs: Any) -> dict[str, Any]:
        if self._conn is None:
            self.connect()
        try:
            assert self._conn is not None
            return self._conn.call(func_name, **kwargs)
        except Exception as exc:  # pragma: no cover
            raise SAPRFCError(f"RFC {func_name} fallo: {exc}") from exc
