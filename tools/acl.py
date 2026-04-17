"""
UniFi ACL Rules (Access Control)

Endpoints:
  GET    /v1/sites/{siteId}/acl-rules
  GET    /v1/sites/{siteId}/acl-rules/{aclRuleId}
  POST   /v1/sites/{siteId}/acl-rules
  PUT    /v1/sites/{siteId}/acl-rules/{aclRuleId}
  DELETE /v1/sites/{siteId}/acl-rules/{aclRuleId}
  GET    /v1/sites/{siteId}/acl-rules/ordering
  PUT    /v1/sites/{siteId}/acl-rules/ordering
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_acl_rules",
        description="List all ACL rules on a site.",
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
        name="get_acl_rule",
        description="Get a specific ACL rule.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "aclRuleId": {"type": "string"},
            },
            "required": ["siteId", "aclRuleId"],
        },
    ),
    types.Tool(
        name="create_acl_rule",
        description="Create a new user-defined ACL rule. type: IPV4 or MAC. action: ALLOW or BLOCK.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":               {"type": "string"},
                "type":                 {"type": "string", "enum": ["IPV4", "MAC"]},
                "enabled":              {"type": "boolean"},
                "name":                 {"type": "string"},
                "description":          {"type": "string"},
                "action":               {"type": "string", "enum": ["ALLOW", "BLOCK"]},
                "enforcingDeviceFilter":{"type": "object", "description": "{type, deviceIds}"},
                "sourceFilter":         {"type": "object"},
                "destinationFilter":    {"type": "object"},
                "protocolFilter":       {"type": "array", "items": {"type": "string"},
                                         "description": "TCP, UDP, or omit for all"},
            },
            "required": ["siteId", "type", "enabled", "name", "action"],
        },
    ),
    types.Tool(
        name="update_acl_rule",
        description="Update an existing user-defined ACL rule.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":               {"type": "string"},
                "aclRuleId":            {"type": "string"},
                "type":                 {"type": "string", "enum": ["IPV4", "MAC"]},
                "enabled":              {"type": "boolean"},
                "name":                 {"type": "string"},
                "description":          {"type": "string"},
                "action":               {"type": "string", "enum": ["ALLOW", "BLOCK"]},
                "enforcingDeviceFilter":{"type": "object"},
                "sourceFilter":         {"type": "object"},
                "destinationFilter":    {"type": "object"},
                "protocolFilter":       {"type": "array", "items": {"type": "string"}},
            },
            "required": ["siteId", "aclRuleId", "type", "enabled", "name", "action"],
        },
    ),
    types.Tool(
        name="delete_acl_rule",
        description="Delete a user-defined ACL rule from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":    {"type": "string"},
                "aclRuleId": {"type": "string"},
            },
            "required": ["siteId", "aclRuleId"],
        },
    ),
    types.Tool(
        name="get_acl_rule_ordering",
        description="Get the ordering of user-defined ACL rules on a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
            },
            "required": ["siteId"],
        },
    ),
    types.Tool(
        name="update_acl_rule_ordering",
        description="Reorder user-defined ACL rules on a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":            {"type": "string"},
                "orderedAclRuleIds": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["siteId", "orderedAclRuleIds"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_acl_rules":
        return api("GET", f"/sites/{a['siteId']}/acl-rules", params=omit(a, "siteId"))

    elif name == "get_acl_rule":
        return api("GET", f"/sites/{a['siteId']}/acl-rules/{a['aclRuleId']}")

    elif name == "create_acl_rule":
        return api("POST", f"/sites/{a['siteId']}/acl-rules", body=omit(a, "siteId"))

    elif name == "update_acl_rule":
        return api("PUT", f"/sites/{a['siteId']}/acl-rules/{a['aclRuleId']}",
                   body=omit(a, "siteId", "aclRuleId"))

    elif name == "delete_acl_rule":
        return api("DELETE", f"/sites/{a['siteId']}/acl-rules/{a['aclRuleId']}")

    elif name == "get_acl_rule_ordering":
        return api("GET", f"/sites/{a['siteId']}/acl-rules/ordering")

    elif name == "update_acl_rule_ordering":
        return api("PUT", f"/sites/{a['siteId']}/acl-rules/ordering",
                   body={"orderedAclRuleIds": a["orderedAclRuleIds"]})
