"""
UniFi Devices

Endpoints:
  GET    /v1/sites/{siteId}/devices
  POST   /v1/sites/{siteId}/devices
  GET    /v1/sites/{siteId}/devices/{deviceId}
  DELETE /v1/sites/{siteId}/devices/{deviceId}
  GET    /v1/sites/{siteId}/devices/{deviceId}/statistics/latest
  POST   /v1/sites/{siteId}/devices/{deviceId}/actions
  POST   /v1/sites/{siteId}/devices/{deviceId}/interfaces/ports/{portIdx}/actions
  GET    /v1/pending-devices
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_adopted_devices",
        description="List all adopted devices on a site.",
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
        name="adopt_device",
        description="Adopt a device to a site by MAC address.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":            {"type": "string"},
                "macAddress":        {"type": "string", "description": "Device MAC address"},
                "ignoreDeviceLimit": {"type": "boolean"},
            },
            "required": ["siteId", "macAddress", "ignoreDeviceLimit"],
        },
    ),
    types.Tool(
        name="get_adopted_device",
        description="Get detailed info about an adopted device (firmware, uplink, ports, radios).",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "deviceId": {"type": "string"},
            },
            "required": ["siteId", "deviceId"],
        },
    ),
    types.Tool(
        name="remove_device",
        description="Remove (unadopt) a device from a site. Online devices reset to factory defaults.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "deviceId": {"type": "string"},
            },
            "required": ["siteId", "deviceId"],
        },
    ),
    types.Tool(
        name="get_device_statistics",
        description="Get latest real-time stats for a device: uptime, CPU, memory, tx/rx rates.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "deviceId": {"type": "string"},
            },
            "required": ["siteId", "deviceId"],
        },
    ),
    types.Tool(
        name="execute_device_action",
        description="Execute an action on an adopted device. Supported action: RESTART.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "deviceId": {"type": "string"},
                "action":   {"type": "string", "enum": ["RESTART"]},
            },
            "required": ["siteId", "deviceId", "action"],
        },
    ),
    types.Tool(
        name="execute_port_action",
        description="Execute an action on a device port. Supported action: POWER_CYCLE.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":   {"type": "string"},
                "deviceId": {"type": "string"},
                "portIdx":  {"type": "integer", "description": "Port index"},
                "action":   {"type": "string", "enum": ["POWER_CYCLE"]},
            },
            "required": ["siteId", "deviceId", "portIdx", "action"],
        },
    ),
    types.Tool(
        name="list_pending_devices",
        description="List devices pending adoption across the controller.",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {"type": "integer"},
                "limit":  {"type": "integer"},
                "filter": {"type": "string"},
            },
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_adopted_devices":
        return api("GET", f"/sites/{a['siteId']}/devices", params=omit(a, "siteId"))

    elif name == "adopt_device":
        return api("POST", f"/sites/{a['siteId']}/devices", body=omit(a, "siteId"))

    elif name == "get_adopted_device":
        return api("GET", f"/sites/{a['siteId']}/devices/{a['deviceId']}")

    elif name == "remove_device":
        return api("DELETE", f"/sites/{a['siteId']}/devices/{a['deviceId']}")

    elif name == "get_device_statistics":
        return api("GET", f"/sites/{a['siteId']}/devices/{a['deviceId']}/statistics/latest")

    elif name == "execute_device_action":
        return api("POST", f"/sites/{a['siteId']}/devices/{a['deviceId']}/actions",
                   body={"action": a["action"]})

    elif name == "execute_port_action":
        return api(
            "POST",
            f"/sites/{a['siteId']}/devices/{a['deviceId']}/interfaces/ports/{a['portIdx']}/actions",
            body={"action": a["action"]},
        )

    elif name == "list_pending_devices":
        return api("GET", "/pending-devices", params=omit(a))
