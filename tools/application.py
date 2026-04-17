"""Application Info — GET /v1/info"""

from typing import Any
import mcp.types as types
from client import api

TOOLS = [
    types.Tool(
        name="get_application_info",
        description="Get UniFi Network application version info.",
        inputSchema={"type": "object", "properties": {}},
    ),
]

TOOL_NAMES = {t.name for t in TOOLS}


def dispatch(name: str, a: dict) -> Any:
    if name == "get_application_info":
        return api("GET", "/info")
