# UniFi Network MCP Server

Docker-hosted MCP server for managing Ubiquiti UniFi Network infrastructure.
Covers all 62 endpoints from UniFi Network API v10.1.84.

Transport: **SSE** (`http://localhost:8000/sse`) — persistent container, no subprocess spawning.

## Prerequisites

- Docker (with Compose)
- UniFi Network controller reachable on your local network
- UniFi API key

## Generate an API Key

**UniFi Site Manager:** [unifi.ui.com](https://unifi.ui.com) → **API** → **Create API Key**

**Local controller:** Settings → Control Plane → Integrations → API Keys

> The key is shown only once — copy it immediately.

## Quick Start

```bash
git clone https://github.com/NigelVanHattum/unifi-mcp.git
cd unifi-mcp

# Configure credentials
mkdir -p ~/.config/unifi-mcp
cat > ~/.config/unifi-mcp/config.json << 'EOF'
{
  "host": "192.168.1.1",
  "api_key": "your-api-key-here",
  "verify_ssl": false
}
EOF

# Start the server
docker compose up -d
```

The server is now running at `http://localhost:8000`. Verify:

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```

## Connect to Claude

### Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "unifi-network": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

Restart Claude Desktop. Ask: _"List my UniFi sites"_

### Claude Code

```bash
claude mcp add unifi-network --url http://localhost:8000/sse
```

## Configuration

Credentials are loaded in this order (first found wins):

| Priority | Method | Details |
|---|---|---|
| 1 | Config file | Mount `/config/config.json` via Docker volume |
| 2 | Environment vars | `UNIFI_HOST`, `UNIFI_API_KEY`, `UNIFI_VERIFY_SSL` |

### Config file (recommended)

Default volume mount: `~/.config/unifi-mcp` → `/config` (read-only)

```json
{
  "host": "192.168.1.1",
  "api_key": "your-api-key-here",
  "verify_ssl": false
}
```

### Environment variables

Copy `.env.example` to `.env`, fill in values, then `docker compose up -d`.

## Server Options

| Variable | Default | Description |
|---|---|---|
| `SERVER_HOST` | `0.0.0.0` | Bind address |
| `SERVER_PORT` | `8000` | Port |

## Tools Reference

| Group | Tools |
|---|---|
| Application | `get_application_info` |
| Sites | `list_sites` |
| Devices | `list_adopted_devices`, `adopt_device`, `get_adopted_device`, `remove_device`, `get_device_statistics`, `execute_device_action`, `execute_port_action`, `list_pending_devices` |
| Clients | `list_clients`, `get_client`, `execute_client_action` |
| Networks | `list_networks`, `create_network`, `get_network`, `update_network`, `delete_network`, `get_network_references` |
| WiFi | `list_wifi_broadcasts`, `create_wifi_broadcast`, `get_wifi_broadcast`, `update_wifi_broadcast`, `delete_wifi_broadcast` |
| Hotspot | `list_vouchers`, `create_vouchers`, `delete_vouchers`, `get_voucher`, `delete_voucher` |
| Firewall | `list_firewall_zones`, `get_firewall_zone`, `create_firewall_zone`, `update_firewall_zone`, `delete_firewall_zone`, `list_firewall_policies`, `get_firewall_policy`, `create_firewall_policy`, `update_firewall_policy`, `delete_firewall_policy`, `patch_firewall_policy`, `get_firewall_policy_ordering`, `update_firewall_policy_ordering` |
| ACL Rules | `list_acl_rules`, `get_acl_rule`, `create_acl_rule`, `update_acl_rule`, `delete_acl_rule`, `get_acl_rule_ordering`, `update_acl_rule_ordering` |
| DNS Policies | `list_dns_policies`, `get_dns_policy`, `create_dns_policy`, `update_dns_policy`, `delete_dns_policy` |
| Traffic Lists | `list_traffic_matching_lists`, `get_traffic_matching_list`, `create_traffic_matching_list`, `update_traffic_matching_list`, `delete_traffic_matching_list` |
| Supporting | `list_wan_interfaces`, `list_site_to_site_vpn_tunnels`, `list_vpn_servers` |

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Build image locally (runs tests in build stage — fails if tests fail)
docker build -t unifi-mcp .

# Start via compose
docker compose up
```

## API Reference

[UniFi Network API v10.1.84](https://developer.ui.com/network/v10.1.84/gettingstarted)
