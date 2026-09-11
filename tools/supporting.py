"""UniFi Supporting Resources

Endpoints:
  GET /v1/countries
  GET /v1/dpi/applications
  GET /v1/dpi/categories
  GET /v1/sites/{siteId}/wans
  GET /v1/sites/{siteId}/vpn/site-to-site-tunnels
  GET /v1/sites/{siteId}/vpn/servers
  GET /v1/sites/{siteId}/device-tags
  GET /v1/sites/{siteId}/radius/profiles
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    # ── Global resources (no siteId) ────────────────────────────────────────
    types.Tool(
        name="list_countries",
        description="List all countries recognized by the UniFi controller.",
        input_schema={
            "type": "object",
            "properties": {
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
                "filter": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="list_dpi_applications",
        description="List all DPI application signatures known to the UniFi controller.",
        input_schema={
            "type": "object",
            "properties": {
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
                "filter": {"type": "string"},
            },
        },
    ),
    types.Tool(
        name="list_dpi_categories",
        description="List all DPI application categories known to the UniFi controller.",
        input_schema={
            "type": "object",
            "properties": {
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
                "filter": {"type": "string"},
            },
        },
    ),
    # ── Site-scoped resources ─────────────────────────────────────────────
    types.Tool(
        name="list_wan_interfaces",
        description="List WAN interface definitions for a site (useful for NAT/network config).",
        input_schema={
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
        input_schema={
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
        input_schema={
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
        name="list_device_tags",
        description="List all device tags on a site.",
        input_schema={
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
        name="list_radius_profiles",
        description="List all RADIUS server profiles on a site.",
        input_schema={
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
    if name == "list_countries":
        return api("GET", "/countries", params=omit(a))

    elif name == "list_dpi_applications":
        return api("GET", "/dpi/applications", params=omit(a))

    elif name == "list_dpi_categories":
        return api("GET", "/dpi/categories", params=omit(a))

    elif name == "list_wan_interfaces":
        return api("GET", f"/sites/{a['siteId']}/wans", params=omit(a, "siteId"))

    elif name == "list_site_to_site_vpn_tunnels":
        return api("GET", f"/sites/{a['siteId']}/vpn/site-to-site-tunnels",
                   params=omit(a, "siteId"))

    elif name == "list_vpn_servers":
        return api("GET", f"/sites/{a['siteId']}/vpn/servers", params=omit(a, "siteId"))

    elif name == "list_device_tags":
        return api("GET", f"/sites/{a['siteId']}/device-tags",
                   params=omit(a, "siteId"))

    elif name == "list_radius_profiles":
        return api("GET", f"/sites/{a['siteId']}/radius/profiles",
                   params=omit(a, "siteId"))