"""Tool modules for UniFi Network MCP server."""

from . import (
    application,
    sites,
    devices,
    clients,
    networks,
    wifi,
    hotspot,
    firewall,
    acl,
    dns,
    traffic,
    supporting,
)

_MODULES = [
    application,
    sites,
    devices,
    clients,
    networks,
    wifi,
    hotspot,
    firewall,
    acl,
    dns,
    traffic,
    supporting,
]

# Aggregated tool list for MCP registration
ALL_TOOLS = [tool for mod in _MODULES for tool in mod.TOOLS]


def dispatch(name: str, args: dict):
    """Route tool call to the correct module dispatcher."""
    for mod in _MODULES:
        if name in mod.TOOL_NAMES:
            return mod.dispatch(name, args)
    raise ValueError(f"Unknown tool: {name}")
