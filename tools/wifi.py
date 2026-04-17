"""
UniFi WiFi Broadcasts

Endpoints:
  GET    /v1/sites/{siteId}/wifi/broadcasts
  POST   /v1/sites/{siteId}/wifi/broadcasts
  GET    /v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}
  PUT    /v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}
  DELETE /v1/sites/{siteId}/wifi/broadcasts/{wifiBroadcastId}
"""

from typing import Any
import mcp.types as types
from client import api, omit

_BROADCAST_PROPS = {
    "siteId":                             {"type": "string"},
    "type":                               {"type": "string", "enum": ["STANDARD", "IOT_OPTIMIZED"]},
    "name":                               {"type": "string", "description": "SSID name"},
    "enabled":                            {"type": "boolean"},
    "network":                            {"type": "object"},
    "securityConfiguration":              {"type": "object"},
    "broadcastingDeviceFilter":           {"type": "object"},
    "mdnsProxyConfiguration":             {"type": "object"},
    "multicastFilteringPolicy":           {"type": "object"},
    "multicastToUnicastConversionEnabled":{"type": "boolean"},
    "clientIsolationEnabled":             {"type": "boolean"},
    "hideName":                           {"type": "boolean"},
    "uapsdEnabled":                       {"type": "boolean"},
    "basicDataRateKbpsByFrequencyGHz":    {"type": "object"},
    "clientFilteringPolicy":              {"type": "object"},
    "blackoutScheduleConfiguration":      {"type": "object"},
    "broadcastingFrequenciesGHz":         {"type": "array", "items": {"type": "number"}},
    "hotspotConfiguration":               {"type": "object"},
    "mloEnabled":                         {"type": "boolean"},
    "bandSteeringEnabled":                {"type": "boolean"},
    "arpProxyEnabled":                    {"type": "boolean"},
    "bssTransitionEnabled":               {"type": "boolean"},
    "advertiseDeviceName":                {"type": "boolean"},
    "dtimPeriodByFrequencyGHzOverride":   {"type": "object"},
}

_BROADCAST_REQUIRED = [
    "siteId", "type", "name", "enabled", "securityConfiguration",
    "multicastToUnicastConversionEnabled", "clientIsolationEnabled",
    "hideName", "uapsdEnabled",
]

TOOLS = [
    types.Tool(
        name="list_wifi_broadcasts",
        description="List all WiFi broadcasts (SSIDs) on a site.",
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
        name="create_wifi_broadcast",
        description="Create a new WiFi broadcast (SSID) on a site. type: STANDARD or IOT_OPTIMIZED.",
        inputSchema={
            "type": "object",
            "properties": _BROADCAST_PROPS,
            "required": _BROADCAST_REQUIRED,
        },
    ),
    types.Tool(
        name="get_wifi_broadcast",
        description="Get detailed info about a WiFi broadcast.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":          {"type": "string"},
                "wifiBroadcastId": {"type": "string"},
            },
            "required": ["siteId", "wifiBroadcastId"],
        },
    ),
    types.Tool(
        name="update_wifi_broadcast",
        description="Update an existing WiFi broadcast.",
        inputSchema={
            "type": "object",
            "properties": {
                **_BROADCAST_PROPS,
                "wifiBroadcastId": {"type": "string"},
            },
            "required": ["wifiBroadcastId"] + _BROADCAST_REQUIRED,
        },
    ),
    types.Tool(
        name="delete_wifi_broadcast",
        description="Delete a WiFi broadcast from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":          {"type": "string"},
                "wifiBroadcastId": {"type": "string"},
                "force":           {"type": "boolean"},
            },
            "required": ["siteId", "wifiBroadcastId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_wifi_broadcasts":
        return api("GET", f"/sites/{a['siteId']}/wifi/broadcasts", params=omit(a, "siteId"))

    elif name == "create_wifi_broadcast":
        return api("POST", f"/sites/{a['siteId']}/wifi/broadcasts", body=omit(a, "siteId"))

    elif name == "get_wifi_broadcast":
        return api("GET", f"/sites/{a['siteId']}/wifi/broadcasts/{a['wifiBroadcastId']}")

    elif name == "update_wifi_broadcast":
        return api("PUT", f"/sites/{a['siteId']}/wifi/broadcasts/{a['wifiBroadcastId']}",
                   body=omit(a, "siteId", "wifiBroadcastId"))

    elif name == "delete_wifi_broadcast":
        return api("DELETE", f"/sites/{a['siteId']}/wifi/broadcasts/{a['wifiBroadcastId']}",
                   params={"force": a.get("force")})
