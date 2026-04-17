#!/usr/bin/env python3
"""
UniFi Network MCP Server
Covers all UniFi Network API v10.1.84 endpoints (local connection type).

Configuration (environment variables):
  UNIFI_HOST       - Controller IP or hostname (default: 192.168.1.1)
  UNIFI_API_KEY    - API key from UniFi Site Manager
  UNIFI_VERIFY_SSL - Set to "true" to verify SSL (default: false)
"""

import json
import asyncio
import httpx
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

import tools

server = Server("unifi-network")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return tools.ALL_TOOLS


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    try:
        result = tools.dispatch(name, arguments)
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    except httpx.HTTPStatusError as e:
        return [types.TextContent(type="text", text=f"HTTP {e.response.status_code}: {e.response.text}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {e}")]


async def main() -> None:
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    asyncio.run(main())
