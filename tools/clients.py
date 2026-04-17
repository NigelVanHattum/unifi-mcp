"""
UniFi Clients

Endpoints:
  GET  /v1/sites/{siteId}/clients
  GET  /v1/sites/{siteId}/clients/{clientId}
  POST /v1/sites/{siteId}/clients/{clientId}/actions
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_clients",
        description="List all connected clients on a site (wired, wireless, VPN).",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
                "filter": {"type": "string"},
            },
            "required": ["siteId"],
        },
    ),
    types.Tool(
        name="get_client",
        description="Get detailed info about a connected client.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "clientId": {"type": "string"},
            },
            "required": ["siteId", "clientId"],
        },
    ),
    types.Tool(
        name="execute_client_action",
        description="Execute an action on a client. Actions: AUTHORIZE_GUEST_ACCESS, UNAUTHORIZE_GUEST_ACCESS.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":               {"type": "string"},
                "clientId":             {"type": "string"},
                "action":               {"type": "string", "enum": ["AUTHORIZE_GUEST_ACCESS", "UNAUTHORIZE_GUEST_ACCESS"]},
                "timeLimitMinutes":     {"type": "integer", "description": "Optional: guest access duration (minutes)"},
                "dataUsageLimitMBytes": {"type": "integer", "description": "Optional: data limit (MB)"},
                "rxRateLimitKbps":      {"type": "integer", "description": "Optional: download rate limit (kbps)"},
                "txRateLimitKbps":      {"type": "integer", "description": "Optional: upload rate limit (kbps)"},
            },
            "required": ["siteId", "clientId", "action"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_clients":
        return api("GET", f"/sites/{a['siteId']}/clients", params=omit(a, "siteId"))

    elif name == "get_client":
        return api("GET", f"/sites/{a['siteId']}/clients/{a['clientId']}")

    elif name == "execute_client_action":
        return api("POST", f"/sites/{a['siteId']}/clients/{a['clientId']}/actions",
                   body=omit(a, "siteId", "clientId"))
