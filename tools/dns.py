"""
UniFi DNS Policies

Endpoints:
  GET    /v1/sites/{siteId}/dns/policies
  GET    /v1/sites/{siteId}/dns/policies/{dnsPolicyId}
  POST   /v1/sites/{siteId}/dns/policies
  PUT    /v1/sites/{siteId}/dns/policies/{dnsPolicyId}
  DELETE /v1/sites/{siteId}/dns/policies/{dnsPolicyId}
"""

from typing import Any
import mcp.types as types
from client import api, omit

_DNS_TYPES = ["A_RECORD", "AAAA_RECORD", "CNAME_RECORD", "MX_RECORD",
              "TXT_RECORD", "SRV_RECORD", "FORWARD_DOMAIN"]

TOOLS = [
    types.Tool(
        name="list_dns_policies",
        description="List all DNS policies on a site.",
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
        name="get_dns_policy",
        description="Get a specific DNS policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":      {"type": "string"},
                "dnsPolicyId": {"type": "string"},
            },
            "required": ["siteId", "dnsPolicyId"],
        },
    ),
    types.Tool(
        name="create_dns_policy",
        description="Create a DNS policy. Types: A_RECORD, AAAA_RECORD, CNAME_RECORD, MX_RECORD, TXT_RECORD, SRV_RECORD, FORWARD_DOMAIN.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":      {"type": "string"},
                "type":        {"type": "string", "enum": _DNS_TYPES},
                "enabled":     {"type": "boolean"},
                "domain":      {"type": "string"},
                "ipv4Address": {"type": "string"},
                "ttlSeconds":  {"type": "integer"},
            },
            "required": ["siteId", "type", "enabled"],
        },
    ),
    types.Tool(
        name="update_dns_policy",
        description="Update an existing DNS policy.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":      {"type": "string"},
                "dnsPolicyId": {"type": "string"},
                "type":        {"type": "string", "enum": _DNS_TYPES},
                "enabled":     {"type": "boolean"},
                "domain":      {"type": "string"},
                "ipv4Address": {"type": "string"},
                "ttlSeconds":  {"type": "integer"},
            },
            "required": ["siteId", "dnsPolicyId", "type", "enabled"],
        },
    ),
    types.Tool(
        name="delete_dns_policy",
        description="Delete a DNS policy from a site.",
        inputSchema={
            "type": "object",
            "properties": {
                "siteId":      {"type": "string"},
                "dnsPolicyId": {"type": "string"},
            },
            "required": ["siteId", "dnsPolicyId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_dns_policies":
        return api("GET", f"/sites/{a['siteId']}/dns/policies", params=omit(a, "siteId"))

    elif name == "get_dns_policy":
        return api("GET", f"/sites/{a['siteId']}/dns/policies/{a['dnsPolicyId']}")

    elif name == "create_dns_policy":
        return api("POST", f"/sites/{a['siteId']}/dns/policies", body=omit(a, "siteId"))

    elif name == "update_dns_policy":
        return api("PUT", f"/sites/{a['siteId']}/dns/policies/{a['dnsPolicyId']}",
                   body=omit(a, "siteId", "dnsPolicyId"))

    elif name == "delete_dns_policy":
        return api("DELETE", f"/sites/{a['siteId']}/dns/policies/{a['dnsPolicyId']}")
