"""
HTTP client and configuration for UniFi Network API (local connection).

Config resolution order (first found wins):
  1. /config/config.json  — Docker volume mount (-v /host/path:/config:ro)
  2. Environment variables — UNIFI_HOST / UNIFI_API_KEY / UNIFI_VERIFY_SSL

Environment variables:
  UNIFI_HOST       - Controller IP or hostname (default: 192.168.1.1)
  UNIFI_API_KEY    - API key from UniFi Site Manager
  UNIFI_VERIFY_SSL - "true" to verify TLS cert (default: false)
"""

import json
import os
from pathlib import Path
from typing import Any

import httpx


def _load_config() -> dict:
    """Load config from Docker volume mount or environment variables."""
    config_file = Path("/config/config.json")
    if config_file.exists():
        try:
            return json.loads(config_file.read_text())
        except Exception:
            pass

    return {
        "host":       os.environ.get("UNIFI_HOST", "192.168.1.1"),
        "api_key":    os.environ.get("UNIFI_API_KEY", ""),
        "verify_ssl": os.environ.get("UNIFI_VERIFY_SSL", "false").lower() == "true",
    }


_cfg = _load_config()

UNIFI_HOST       = _cfg.get("host", "192.168.1.1")
UNIFI_API_KEY    = _cfg.get("api_key", "")
UNIFI_VERIFY_SSL = _cfg.get("verify_ssl", False)

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
