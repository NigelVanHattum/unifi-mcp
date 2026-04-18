"""
HTTP client and configuration for UniFi Network API (local connection).

Config resolution order (first found wins):
  1. $CLAUDE_PLUGIN_ROOT/unifi-config.json  (plugin root — written by setup skill)
  2. ~/.config/unifi-mcp/config.json        (user config dir — written by setup skill)
  3. /config/config.json                    (Docker volume mount)
  4. Environment variables                   (manual / Claude Desktop / docker -e)
  5. Built-in defaults

Environment variables (when not using config file):
  UNIFI_HOST       - Controller IP or hostname (default: 192.168.1.1)
  UNIFI_API_KEY    - API key from UniFi Site Manager
  UNIFI_VERIFY_SSL - "true" to verify TLS (default: false)
"""

import json
import os
from pathlib import Path
from typing import Any

import httpx


def _load_config() -> dict:
    """Load config from file (plugin root or ~/.config) or env vars."""
    # 1. Plugin root (set by Claude when MCP server process starts)
    plugin_root = os.environ.get("CLAUDE_PLUGIN_ROOT", "")
    if plugin_root:
        config_path = Path(plugin_root) / "unifi-config.json"
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except Exception:
                pass

    # 2. User config dir (written by setup skill via Cowork file access)
    user_config = Path.home() / ".config" / "unifi-mcp" / "config.json"
    if user_config.exists():
        try:
            return json.loads(user_config.read_text())
        except Exception:
            pass

    # 3. Docker volume mount (-v ~/.config/unifi-mcp:/config:ro)
    docker_config = Path("/config/config.json")
    if docker_config.exists():
        try:
            return json.loads(docker_config.read_text())
        except Exception:
            pass

    # 4. Environment variables
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
