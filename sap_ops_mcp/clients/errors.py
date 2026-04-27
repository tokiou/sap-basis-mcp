class SAPClientError(Exception):
    """Error base para el cliente SAP."""


class SAPConnectionError(SAPClientError):
    """Error al conectar con SAP."""


class SAPRFCError(SAPClientError):
    """Error al ejecutar llamadas RFC."""
