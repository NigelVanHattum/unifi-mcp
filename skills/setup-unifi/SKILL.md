---
name: setup-unifi
description: >
  Configure the UniFi MCP connector with controller credentials. Use when the user
  says "setup UniFi", "configure UniFi", "connect to UniFi", "set UniFi API key",
  "UniFi not working", or asks how to connect to their UniFi controller.
---

# Setup UniFi Connector

Guide the user through configuring credentials for the UniFi Network MCP server.
Credentials are written to `unifi-config.json` in the plugin root directory.

## Steps

1. Ask the user for the following values:
   - **Controller host** — IP address or hostname of their UniFi Network controller (e.g. `192.168.1.1` or `unifi.local`)
   - **API key** — from UniFi Site Manager → API → Create API Key (or local controller: Settings → Control Plane → Integrations → API Keys)
   - **Verify SSL** — whether to verify the controller's TLS certificate (default: `false` — controllers use self-signed certs)

2. Write the config file using the Bash tool:

```bash
cat > "${CLAUDE_PLUGIN_ROOT}/unifi-config.json" << 'JSONEOF'
{
  "host": "<UNIFI_HOST>",
  "api_key": "<UNIFI_API_KEY>",
  "verify_ssl": false
}
JSONEOF
```

Replace `<UNIFI_HOST>` and `<UNIFI_API_KEY>` with the values the user provided.
Set `"verify_ssl": true` only if the user explicitly requested it.

3. Confirm the file was written:

```bash
cat "${CLAUDE_PLUGIN_ROOT}/unifi-config.json"
```

4. Tell the user: **Restart Claude** (fully quit and relaunch) so the MCP server picks up the new config.

5. After restart, verify the connection by calling the `get_application_info` tool and reporting the result.

## Security Notes

- The config file is stored in the plugin directory on the user's local machine.
- The API key is stored in plaintext — standard for local MCP configs.
- Never log or display the API key in full after it's been saved.
