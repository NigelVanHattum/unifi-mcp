"""Sites — GET /v1/sites"""

from typing import Any
import mcp.types as types
from client import api, omit

TOOLS = [
    types.Tool(
        name="list_sites",
        description="List all local sites managed by this Network application.",
        inputSchema={
            "type": "object",
            "properties": {
                "offset": {"type": "integer", "description": "Pagination offset (default 0)"},
                "limit":  {"type": "integer", "description": "Page size (default 25)"},
                "filter": {"type": "string",  "description": "Filter expression"},
            },
        },
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "list_sites":
        return api("GET", "/sites", params=omit(a))
