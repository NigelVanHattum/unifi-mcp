"""
UniFi Firewall (Zones + Policies)

Endpoints:
  GET    /v1/sites/{siteId}/firewall/zones
  GET    /v1/sites/{siteId}/firewall/zones/{firewallZoneId}
  POST   /v1/sites/{siteId}/firewall/zones
  PUT    /v1/sites/{siteId}/firewall/zones/{firewallZoneId}
  DELETE /v1/sites/{siteId}/firewall/zones/{firewallZoneId}
  GET    /v1/sites/{siteId}/firewall/policies
  GET    /v1/sites/{siteId}/firewall/policies/{firewallPolicyId}
  POST   /v1/sites/{siteId}/firewall/policies
  PUT    /v1/sites/{siteId}/firewall/policies/{firewallPolicyId}
  DELETE /v1/sites/{siteId}/firewall/policies/{firewallPolicyId}
  PATCH  /v1/sites/{siteId}/firewall/policies/{firewallPolicyId}
  GET    /v1/sites/{siteId}/firewall/policies/ordering
  PUT    /v1/sites/{siteId}/firewall/policies/ordering
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    # ── Zones ──────────────────────────────────────────────────────────────
    types.Tool(
        name="list_firewall_zones",
        description="List all firewall zones on a site.",
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
        name="get_firewall_zone",
        description="Get a specific firewall zone.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":         {"type": "string"},
                "firewallZoneId": {"type": "string"},
            },
            "required": ["siteId", "firewallZoneId"],
        },
    ),
    types.Tool(
        name="create_firewall_zone",
        description="Create a new custom firewall zone on a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":     {"type": "string"},
                "name":       {"type": "string"},
                "networkIds": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["siteId", "name", "networkIds"],
        },
    ),
    types.Tool(
        name="update_firewall_zone",
        description="Update a firewall zone.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":         {"type": "string"},
                "firewallZoneId": {"type": "string"},
                "name":           {"type": "string"},
                "networkIds":     {"type": "array", "items": {"type": "string"}},
            },
            "required": ["siteId", "firewallZoneId", "name", "networkIds"],
        },
    ),
    types.Tool(
        name="delete_firewall_zone",
        description="Delete a custom firewall zone from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":         {"type": "string"},
                "firewallZoneId": {"type": "string"},
            },
            "required": ["siteId", "firewallZoneId"],
        },
    ),

    # ── Policies ───────────────────────────────────────────────────────────
    types.Tool(
        name="list_firewall_policies",
        description="List all firewall policies on a site.",
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
        name="get_firewall_policy",
        description="Get a specific firewall policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":           {"type": "string"},
                "firewallPolicyId": {"type": "string"},
            },
            "required": ["siteId", "firewallPolicyId"],
        },
    ),
    types.Tool(
        name="create_firewall_policy",
        description="Create a new firewall policy. action.type: ALLOW, BLOCK, or REJECT.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                {"type": "string"},
                "enabled":               {"type": "boolean"},
                "name":                  {"type": "string"},
                "description":           {"type": "string"},
                "action":                {"type": "object", "description": "{type: ALLOW|BLOCK|REJECT}"},
                "source":                {"type": "object", "description": "{zoneId, trafficFilter}"},
                "destination":           {"type": "object", "description": "{zoneId, trafficFilter}"},
                "ipProtocolScope":       {"type": "object", "description": "{ipVersion, protocol}"},
                "connectionStateFilter": {"type": "array", "items": {"type": "string"},
                                         "description": "NEW, INVALID, ESTABLISHED, RELATED"},
                "ipsecFilter":           {"type": "string", "enum": ["MATCH_ENCRYPTED", "MATCH_NOT_ENCRYPTED"]},
                "loggingEnabled":        {"type": "boolean"},
                "schedule":              {"type": "object"},
            },
            "required": ["siteId", "enabled", "name", "action", "source", "destination",
                         "ipProtocolScope", "loggingEnabled"],
        },
    ),
    types.Tool(
        name="update_firewall_policy",
        description="Update an existing firewall policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                {"type": "string"},
                "firewallPolicyId":      {"type": "string"},
                "enabled":               {"type": "boolean"},
                "name":                  {"type": "string"},
                "description":           {"type": "string"},
                "action":                {"type": "object"},
                "source":                {"type": "object"},
                "destination":           {"type": "object"},
                "ipProtocolScope":       {"type": "object"},
                "connectionStateFilter": {"type": "array", "items": {"type": "string"}},
                "ipsecFilter":           {"type": "string", "enum": ["MATCH_ENCRYPTED", "MATCH_NOT_ENCRYPTED"]},
                "loggingEnabled":        {"type": "boolean"},
                "schedule":              {"type": "object"},
            },
            "required": ["siteId", "firewallPolicyId", "enabled", "name", "action",
                         "source", "destination", "ipProtocolScope", "loggingEnabled"],
        },
    ),
    types.Tool(
        name="delete_firewall_policy",
        description="Delete a firewall policy from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":           {"type": "string"},
                "firewallPolicyId": {"type": "string"},
            },
            "required": ["siteId", "firewallPolicyId"],
        },
    ),
    types.Tool(
        name="patch_firewall_policy",
        description="Partially update a firewall policy (e.g. toggle loggingEnabled only).",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":           {"type": "string"},
                "firewallPolicyId": {"type": "string"},
                "loggingEnabled":   {"type": "boolean"},
            },
            "required": ["siteId", "firewallPolicyId"],
        },
    ),

    # ── Policy ordering ────────────────────────────────────────────────────
    types.Tool(
        name="get_firewall_policy_ordering",
        description="Get user-defined firewall policy ordering for a source/destination zone pair.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                   {"type": "string"},
                "sourceFirewallZoneId":      {"type": "string"},
                "destinationFirewallZoneId": {"type": "string"},
            },
            "required": ["siteId", "sourceFirewallZoneId", "destinationFirewallZoneId"],
        },
    ),
    types.Tool(
        name="update_firewall_policy_ordering",
        description="Reorder user-defined firewall policies for a source/destination zone pair.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":                   {"type": "string"},
                "sourceFirewallZoneId":      {"type": "string"},
                "destinationFirewallZoneId": {"type": "string"},
                "orderedFirewallPolicyIds":  {
                    "type": "object",
                    "description": "{beforeSystemDefined: [...], afterSystemDefined: [...]}",
                },
            },
            "required": ["siteId", "sourceFirewallZoneId", "destinationFirewallZoneId",
                         "orderedFirewallPolicyIds"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    # Zones
    if name == "list_firewall_zones":
        return api("GET", f"/sites/{a['siteId']}/firewall/zones", params=omit(a, "siteId"))

    elif name == "get_firewall_zone":
        return api("GET", f"/sites/{a['siteId']}/firewall/zones/{a['firewallZoneId']}")

    elif name == "create_firewall_zone":
        return api("POST", f"/sites/{a['siteId']}/firewall/zones", body=omit(a, "siteId"))

    elif name == "update_firewall_zone":
        return api("PUT", f"/sites/{a['siteId']}/firewall/zones/{a['firewallZoneId']}",
                   body=omit(a, "siteId", "firewallZoneId"))

    elif name == "delete_firewall_zone":
        return api("DELETE", f"/sites/{a['siteId']}/firewall/zones/{a['firewallZoneId']}")

    # Policies
    elif name == "list_firewall_policies":
        return api("GET", f"/sites/{a['siteId']}/firewall/policies", params=omit(a, "siteId"))

    elif name == "get_firewall_policy":
        return api("GET", f"/sites/{a['siteId']}/firewall/policies/{a['firewallPolicyId']}")

    elif name == "create_firewall_policy":
        return api("POST", f"/sites/{a['siteId']}/firewall/policies", body=omit(a, "siteId"))

    elif name == "update_firewall_policy":
        return api("PUT", f"/sites/{a['siteId']}/firewall/policies/{a['firewallPolicyId']}",
                   body=omit(a, "siteId", "firewallPolicyId"))

    elif name == "delete_firewall_policy":
        return api("DELETE", f"/sites/{a['siteId']}/firewall/policies/{a['firewallPolicyId']}")

    elif name == "patch_firewall_policy":
        return api("PATCH", f"/sites/{a['siteId']}/firewall/policies/{a['firewallPolicyId']}",
                   body=omit(a, "siteId", "firewallPolicyId"))

    # Ordering
    elif name == "get_firewall_policy_ordering":
        return api("GET", f"/sites/{a['siteId']}/firewall/policies/ordering",
                   params={
                       "sourceFirewallZoneId":      a["sourceFirewallZoneId"],
                       "destinationFirewallZoneId": a["destinationFirewallZoneId"],
                   })

    elif name == "update_firewall_policy_ordering":
        return api("PUT", f"/sites/{a['siteId']}/firewall/policies/ordering",
                   params={
                       "sourceFirewallZoneId":      a["sourceFirewallZoneId"],
                       "destinationFirewallZoneId": a["destinationFirewallZoneId"],
                   },
                   body={"orderedFirewallPolicyIds": a["orderedFirewallPolicyIds"]})
