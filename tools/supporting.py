"""
UniFi Supporting Resources

Endpoints:
  GET /v1/sites/{siteId}/wans
  GET /v1/sites/{siteId}/vpn/site-to-site-tunnels
  GET /v1/sites/{siteId}/vpn/servers
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_wan_interfaces",
        description="List WAN interface definitions for a site (useful for NAT/network config).",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
            },
            "required": ["siteId"],
        },
    ),
    types.Tool(
        name="list_site_to_site_vpn_tunnels",
        description="List all site-to-site VPN tunnels on a site.",
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
        name="list_vpn_servers",
        description="List all VPN servers on a site.",
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
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_wan_interfaces":
        return api("GET", f"/sites/{a['siteId']}/wans", params=omit(a, "siteId"))

    elif name == "list_site_to_site_vpn_tunnels":
        return api("GET", f"/sites/{a['siteId']}/vpn/site-to-site-tunnels",
                   params=omit(a, "siteId"))

    elif name == "list_vpn_servers":
        return api("GET", f"/sites/{a['siteId']}/vpn/servers", params=omit(a, "siteId"))
