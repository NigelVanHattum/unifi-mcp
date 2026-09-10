"""UniFi Switching — LAGs, MC-LAG Domains, Switch Stacks

Endpoints:
  GET    /v1/sites/{siteId}/switching/lags
  GET    /v1/sites/{siteId}/switching/lags/{lagId}
  GET    /v1/sites/{siteId}/switching/mc-lag-domains
  GET    /v1/sites/{siteId}/switching/mc-lag-domains/{mcLagDomainId}
  GET    /v1/sites/{siteId}/switching/switch-stacks
  GET    /v1/sites/{siteId}/switching/switch-stacks/{switchStackId}
"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    # ── LAGs ───────────────────────────────────────────────────────────────
    types.Tool(
        name="list_lags",
        description="List all LAG (Link Aggregation Group) interfaces on a site.",
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
        name="get_lag",
        description="Get details of a specific LAG (Link Aggregation Group) interface.",
        input_schema={
            "type": "object",
            "properties": {
                "siteId": {"type": "string"},
                "lagId":  {"type": "string"},
            },
            "required": ["siteId", "lagId"],
        },
    ),
    # ── MC-LAG Domains ─────────────────────────────────────────────────────
    types.Tool(
        name="list_mc_lag_domains",
        description="List all MC-LAG (Multi-Chassis LAG) domains on a site.",
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
        name="get_mc_lag_domain",
        description="Get details of a specific MC-LAG (Multi-Chassis LAG) domain.",
        input_schema={
            "type": "object",
            "properties": {
                "siteId":         {"type": "string"},
                "mcLagDomainId": {"type": "string"},
            },
            "required": ["siteId", "mcLagDomainId"],
        },
    ),
    # ── Switch Stacks ──────────────────────────────────────────────────────
    types.Tool(
        name="list_switch_stacks",
        description="List all switch stacks on a site.",
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
        name="get_switch_stack",
        description="Get details of a specific switch stack.",
        input_schema={
            "type": "object",
            "properties": {
                "siteId":       {"type": "string"},
                "switchStackId": {"type": "string"},
            },
            "required": ["siteId", "switchStackId"],
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_lags":
        return api("GET", f"/sites/{a['siteId']}/switching/lags",
                   params=omit(a, "siteId"))

    elif name == "get_lag":
        return api("GET", f"/sites/{a['siteId']}/switching/lags/{a['lagId']}")

    elif name == "list_mc_lag_domains":
        return api("GET", f"/sites/{a['siteId']}/switching/mc-lag-domains",
                   params=omit(a, "siteId"))

    elif name == "get_mc_lag_domain":
        return api("GET",
                   f"/sites/{a['siteId']}/switching/mc-lag-domains/{a['mcLagDomainId']}")

    elif name == "list_switch_stacks":
        return api("GET", f"/sites/{a['siteId']}/switching/switch-stacks",
                   params=omit(a, "siteId"))

    elif name == "get_switch_stack":
        return api("GET",
                   f"/sites/{a['siteId']}/switching/switch-stacks/{a['switchStackId']}")