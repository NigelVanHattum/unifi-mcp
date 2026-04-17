"""
UniFi Hotspot (Vouchers)

Endpoints:
  GET    /v1/sites/{siteId}/hotspot/vouchers
  POST   /v1/sites/{siteId}/hotspot/vouchers
  DELETE /v1/sites/{siteId}/hotspot/vouchers
  GET    /v1/sites/{siteId}/hotspot/vouchers/{voucherId}
  DELETE /v1/sites/{siteId}/hotspot/vouchers/{voucherId}
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_vouchers",
        description="List hotspot vouchers on a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "offset": {"type": "integer"},
                "limit":  {"type": "integer", "description": "Default 100"},
                "filter": {"type": "string"},
            },
            "required": ["siteId"],
        },
    ),
    types.Tool(
        name="create_vouchers",
        description="Generate one or more hotspot vouchers.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":               {"type": "string"},
                "count":                {"type": "integer", "description": "Number of vouchers (default 1)"},
                "name":                 {"type": "string", "description": "Voucher note"},
                "authorizedGuestLimit": {"type": "integer", "description": "Max concurrent guests per voucher"},
                "timeLimitMinutes":     {"type": "integer", "description": "Access duration in minutes"},
                "dataUsageLimitMBytes": {"type": "integer"},
                "rxRateLimitKbps":      {"type": "integer"},
                "txRateLimitKbps":      {"type": "integer"},
            },
            "required": ["siteId", "name", "timeLimitMinutes"],
        },
    ),
    types.Tool(
        name="delete_vouchers",
        description="Delete multiple vouchers by filter expression.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "filter": {"type": "string", "description": "Required filter to select vouchers"},
            },
            "required": ["siteId", "filter"],
        },
    ),
    types.Tool(
        name="get_voucher",
        description="Get details of a specific hotspot voucher.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "voucherId": {"type": "string"},
            },
            "required": ["siteId", "voucherId"],
        },
    ),
    types.Tool(
        name="delete_voucher",
        description="Delete a specific hotspot voucher.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "voucherId": {"type": "string"},
            },
            "required": ["siteId", "voucherId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_vouchers":
        return api("GET", f"/sites/{a['siteId']}/hotspot/vouchers", params=omit(a, "siteId"))

    elif name == "create_vouchers":
        return api("POST", f"/sites/{a['siteId']}/hotspot/vouchers", body=omit(a, "siteId"))

    elif name == "delete_vouchers":
        return api("DELETE", f"/sites/{a['siteId']}/hotspot/vouchers",
                   params={"filter": a["filter"]})

    elif name == "get_voucher":
        return api("GET", f"/sites/{a['siteId']}/hotspot/vouchers/{a['voucherId']}")

    elif name == "delete_voucher":
        return api("DELETE", f"/sites/{a['siteId']}/hotspot/vouchers/{a['voucherId']}")
