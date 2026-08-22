import os

DEFAULT_API_BASE_URL = "https://tools.pepkio.com"
TOOL_ID = "realistic-random-seq-generator"


def get_default_base_url() -> str:
    """Get the API base URL from environment or return default production URL."""
    return os.getenv("PEPKIO_API_BASE_URL", DEFAULT_API_BASE_URL).rstrip("/")


def get_default_api_key(base_url: str | None = None) -> str | None:
    """
    Get the Pepkio API key from environment.
    Checks PEPKIO_API_KEY first.
    If base_url contains 'localtest.me', checks LOCAL_PEPKIO_API_KEY as a fallback.
    """
    api_key = os.getenv("PEPKIO_API_KEY")
    if not api_key:
        target_url = base_url or get_default_base_url()
        if "localtest.me" in target_url:
            api_key = os.getenv("LOCAL_PEPKIO_API_KEY")
    return api_key
