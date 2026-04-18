# UniFi Network MCP Server

MCP server for managing Ubiquiti UniFi Network infrastructure via the local controller API. Covers all 62 endpoints from UniFi Network API v10.1.84.

## Prerequisites

- UniFi Network controller (self-hosted, reachable on local network)
- UniFi API key

## Generate an API Key

1. Open **UniFi Site Manager** → [unifi.ui.com](https://unifi.ui.com)
2. Go to **API** → **Create API Key**
3. Copy the key — it's shown only once

> Local controller: UniFi Network app → **Settings** → **Control Plane** → **Integrations** → **API Keys**

## Installation

### Option A — Claude Plugin (Cowork / Claude Code) ✨ Recommended

1. In Claude, open **Settings** → **Plugins** → **Add from GitHub**
2. Enter: `https://github.com/NigelVanHattum/unifi-mcp`
3. Run the **Setup UniFi** skill to configure credentials

The plugin stores credentials in `~/.config/unifi-mcp/config.json` — never in environment variables.

### Option B — Docker (no Python required)

Pull the pre-built image and run with `docker run -i`:

```bash
# Using config file (recommended)
docker run -i --rm \
  --network=host \
  -v ~/.config/unifi-mcp:/config:ro \
  ghcr.io/nigelvanHattum/unifi-mcp:latest

# Using environment variables
docker run -i --rm \
  --network=host \
  -e UNIFI_HOST=192.168.1.1 \
  -e UNIFI_API_KEY=your-api-key-here \
  ghcr.io/nigelvanHattum/unifi-mcp:latest
```

> `--network=host` lets the container reach your local UniFi controller.
> On Mac, Docker Desktop's host network feature must be enabled (Settings → Resources → Network).

**Claude Desktop config** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "unifi-network": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--network=host",
        "-v", "${HOME}/.config/unifi-mcp:/config:ro",
        "ghcr.io/nigelvanHattum/unifi-mcp:latest"
      ]
    }
  }
}
```

**Claude Code** (manual):

```bash
claude mcp add unifi-network \
  --command docker \
  --args "run -i --rm --network=host -v ${HOME}/.config/unifi-mcp:/config:ro ghcr.io/nigelvanHattum/unifi-mcp:latest"
```

### Option C — Python / uv (manual)

Requires Python 3.11+ and [`uv`](https://docs.astral.sh/uv/getting-started/installation/).

1. Clone the repo:
   ```bash
   git clone https://github.com/NigelVanHattum/unifi-mcp.git
   cd unifi-mcp
   uv sync
   ```

2. Create credentials file:
   ```bash
   mkdir -p ~/.config/unifi-mcp
   cat > ~/.config/unifi-mcp/config.json << 'EOF'
   {
     "host": "192.168.1.1",
     "api_key": "your-api-key-here",
     "verify_ssl": false
   }
   EOF
   ```

3. Add to Claude Desktop config:
   ```json
   {
     "mcpServers": {
       "unifi-network": {
         "command": "uv",
         "args": ["run", "--project", "/path/to/unifi-mcp", "python", "/path/to/unifi-mcp/server.py"]
       }
     }
   }
   ```

## Credential Resolution Order

The server checks these locations in order (first found wins):

| Priority | Location | Use case |
|---|---|---|
| 1 | `$CLAUDE_PLUGIN_ROOT/unifi-config.json` | Claude plugin root |
| 2 | `~/.config/unifi-mcp/config.json` | Claude plugin / manual install |
| 3 | `/config/config.json` | Docker volume mount |
| 4 | `UNIFI_HOST` / `UNIFI_API_KEY` env vars | Docker `-e` / Claude Desktop env block |

## Verify Connection

Ask Claude:
> _"List my UniFi sites"_ or _"Get UniFi application info"_

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
uv sync --extra dev

# Run tests
uv run pytest

# Build Docker image locally
docker build -t unifi-mcp .

# Run server directly (for testing)
UNIFI_HOST=192.168.1.1 UNIFI_API_KEY=your-key uv run python server.py
```

## API Reference

[UniFi Network API v10.1.84](https://developer.ui.com/network/v10.1.84/gettingstarted)
