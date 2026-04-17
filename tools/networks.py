"""
UniFi Networks

Endpoints:
  GET    /v1/sites/{siteId}/networks
  POST   /v1/sites/{siteId}/networks
  GET    /v1/sites/{siteId}/networks/{networkId}
  PUT    /v1/sites/{siteId}/networks/{networkId}
  DELETE /v1/sites/{siteId}/networks/{networkId}
  GET    /v1/sites/{siteId}/networks/{networkId}/references
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_networks",
        description="List all networks on a site.",
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
        name="create_network",
        description="Create a new network on a site. vlanId must be 1 for default, ≥2 for additional.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":       {"type": "string"},
                "management":   {"type": "string", "enum": ["UNMANAGED", "GATEWAY", "SWITCH"]},
                "name":         {"type": "string"},
                "enabled":      {"type": "boolean"},
                "vlanId":       {"type": "integer"},
                "dhcpGuarding": {"type": "object", "description": "DHCP Guarding settings (optional)"},
            },
            "required": ["siteId", "management", "name", "enabled", "vlanId"],
        },
    ),
    types.Tool(
        name="get_network",
        description="Get detailed info about a specific network.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "networkId": {"type": "string"},
            },
            "required": ["siteId", "networkId"],
        },
    ),
    types.Tool(
        name="update_network",
        description="Update an existing network on a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":       {"type": "string"},
                "networkId":    {"type": "string"},
                "management":   {"type": "string", "enum": ["UNMANAGED", "GATEWAY", "SWITCH"]},
                "name":         {"type": "string"},
                "enabled":      {"type": "boolean"},
                "vlanId":       {"type": "integer"},
                "dhcpGuarding": {"type": "object"},
            },
            "required": ["siteId", "networkId", "management", "name", "enabled", "vlanId"],
        },
    ),
    types.Tool(
        name="delete_network",
        description="Delete a network from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "networkId": {"type": "string"},
                "force":     {"type": "boolean", "description": "Force delete (default false)"},
            },
            "required": ["siteId", "networkId"],
        },
    ),
    types.Tool(
        name="get_network_references",
        description="Get references to a network (clients and devices using it).",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "networkId": {"type": "string"},
            },
            "required": ["siteId", "networkId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_networks":
        return api("GET", f"/sites/{a['siteId']}/networks", params=omit(a, "siteId"))

    elif name == "create_network":
        return api("POST", f"/sites/{a['siteId']}/networks", body=omit(a, "siteId"))

    elif name == "get_network":
        return api("GET", f"/sites/{a['siteId']}/networks/{a['networkId']}")

    elif name == "update_network":
        return api("PUT", f"/sites/{a['siteId']}/networks/{a['networkId']}",
                   body=omit(a, "siteId", "networkId"))

    elif name == "delete_network":
        return api("DELETE", f"/sites/{a['siteId']}/networks/{a['networkId']}",
                   params={"force": a.get("force")})

    elif name == "get_network_references":
        return api("GET", f"/sites/{a['siteId']}/networks/{a['networkId']}/references")
