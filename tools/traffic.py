"""
UniFi Traffic Matching Lists

Endpoints:
  GET    /v1/sites/{siteId}/traffic-matching-lists
  GET    /v1/sites/{siteId}/traffic-matching-lists/{trafficMatchingListId}
  POST   /v1/sites/{siteId}/traffic-matching-lists
  PUT    /v1/sites/{siteId}/traffic-matching-lists/{trafficMatchingListId}
  DELETE /v1/sites/{siteId}/traffic-matching-lists/{trafficMatchingListId}
"""

from typing import Any
import mcp.types as types
from client import api, omit

_LIST_TYPES = ["PORTS", "IPV4_ADDRESSES", "IPV6_ADDRESSES"]

TOOLS = [
    types.Tool(
        name="list_traffic_matching_lists",
        description="List all traffic matching lists on a site.",
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
        name="get_traffic_matching_list",
        description="Get a specific traffic matching list.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                {"type": "string"},
                "trafficMatchingListId": {"type": "string"},
            },
            "required": ["siteId", "trafficMatchingListId"],
        },
    ),
    types.Tool(
        name="create_traffic_matching_list",
        description="Create a traffic matching list. Types: PORTS, IPV4_ADDRESSES, IPV6_ADDRESSES.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "type":   {"type": "string", "enum": _LIST_TYPES},
                "name":   {"type": "string"},
                "items":  {"type": "array", "description": "Port ranges or IP addresses"},
            },
            "required": ["siteId", "type", "name"],
        },
    ),
    types.Tool(
        name="update_traffic_matching_list",
        description="Update an existing traffic matching list.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                {"type": "string"},
                "trafficMatchingListId": {"type": "string"},
                "type":                  {"type": "string", "enum": _LIST_TYPES},
                "name":                  {"type": "string"},
                "items":                 {"type": "array"},
            },
            "required": ["siteId", "trafficMatchingListId", "type", "name"],
        },
    ),
    types.Tool(
        name="delete_traffic_matching_list",
        description="Delete a traffic matching list from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                {"type": "string"},
                "trafficMatchingListId": {"type": "string"},
            },
            "required": ["siteId", "trafficMatchingListId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_traffic_matching_lists":
        return api("GET", f"/sites/{a['siteId']}/traffic-matching-lists",
                   params=omit(a, "siteId"))

    elif name == "get_traffic_matching_list":
        return api("GET",
                   f"/sites/{a['siteId']}/traffic-matching-lists/{a['trafficMatchingListId']}")

    elif name == "create_traffic_matching_list":
        return api("POST", f"/sites/{a['siteId']}/traffic-matching-lists",
                   body=omit(a, "siteId"))

    elif name == "update_traffic_matching_list":
        return api("PUT",
                   f"/sites/{a['siteId']}/traffic-matching-lists/{a['trafficMatchingListId']}",
                   body=omit(a, "siteId", "trafficMatchingListId"))

    elif name == "delete_traffic_matching_list":
        return api("DELETE",
                   f"/sites/{a['siteId']}/traffic-matching-lists/{a['trafficMatchingListId']}")
