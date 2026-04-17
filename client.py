"""
HTTP client and configuration for UniFi Network API (local connection).

Environment variables:
  UNIFI_HOST       - Controller IP or hostname (default: 192.168.1.1)
  UNIFI_API_KEY    - API key from UniFi Site Manager
  UNIFI_VERIFY_SSL - "true" to verify TLS (default: false)
"""

import os
from typing import Any

import httpx

UNIFI_HOST = os.environ.get("UNIFI_HOST", "192.168.1.1")
UNIFI_API_KEY = os.environ.get("UNIFI_API_KEY", "")
UNIFI_VERIFY_SSL = os.environ.get("UNIFI_VERIFY_SSL", "false").lower() == "true"

BASE_URL = f"https://{UNIFI_HOST}/proxy/network/integration/v1"


def _make_client() -> httpx.Client:
    return httpx.Client(
        base_url=BASE_URL,
        headers={
            "X-API-Key": UNIFI_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        verify=UNIFI_VERIFY_SSL,
        timeout=30.0,
    )


def api(method: str, path: str, params: dict | None = None, body: dict | None = None) -> Any:
    """Execute an API request and return parsed JSON (or {"status": "success"} for empty responses)."""
    clean_params = {k: v for k, v in (params or {}).items() if v is not None} or None
    with _make_client() as client:
        r = client.request(method=method, url=path, params=clean_params, json=body)
        r.raise_for_status()
        return r.json() if r.content else {"status": "success"}


def omit(d: dict, *keys: str) -> dict:
    """Return dict without specified keys and without None values."""
    return {k: v for k, v in d.items() if k not in keys and v is not None}
