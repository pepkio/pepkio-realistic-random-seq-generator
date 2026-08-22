from typing import Any, Dict, Optional


class PepkioError(Exception):
    """Base exception for Pepkio API errors."""

    pass


class PepkioAuthError(PepkioError):
    """Raised when authentication fails or API key is missing."""

    pass


class PepkioHTTPError(PepkioError):
    """Raised when an HTTP error occurs."""

    def __init__(self, status_code: int, message: str, body: Optional[Any] = None):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.body = body


class PepkioAPIError(PepkioError):
    """Raised when the API returns an error response body."""

    def __init__(self, error_message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(error_message)
        self.error_message = error_message
        self.details = details
