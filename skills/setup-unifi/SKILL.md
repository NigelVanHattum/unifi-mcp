---
name: setup-unifi
description: >
  Configure the UniFi MCP connector with controller credentials. Use when the user
  says "setup UniFi", "configure UniFi", "connect to UniFi", "set UniFi API key",
  "UniFi not working", or asks how to connect to their UniFi controller.
---

# Setup UniFi Connector

Guide the user through configuring credentials for the UniFi Network MCP server.
Credentials are stored in `~/.config/unifi-mcp/config.json` on the user's machine.

## Steps

### 1. Collect credentials

Ask the user for:
- **Controller host** — IP address or hostname (e.g. `192.168.1.1` or `unifi.local`)
- **API key** — from UniFi Site Manager → API → Create API Key, or local controller: Settings → Control Plane → Integrations → API Keys
- **Verify SSL** — whether to verify TLS cert (default: `false` — controllers use self-signed certs)

### 2. Test connection before saving

Verify credentials work before writing anything. Use the Bash tool:

```bash
python3 -c "
import httpx, sys
host = 'UNIFI_HOST_PLACEHOLDER'
api_key = 'UNIFI_API_KEY_PLACEHOLDER'
try:
    r = httpx.get(
        f'https://{host}/proxy/network/integration/v1/sites',
        headers={'X-API-Key': api_key},
        verify=False,
        timeout=10
    )
    r.raise_for_status()
    sites = r.json().get('data', [])
    print(f'OK — {len(sites)} site(s): {[s[\"name\"] for s in sites]}')
except Exception as e:
    print(f'FAIL: {e}', file=sys.stderr)
    sys.exit(1)
"
```

Substitute actual values for the placeholders.
If this fails, report the error and stop — do not save bad credentials.

### 3. Request access to write credentials

Use `request_cowork_directory` to ask the user to select their `~/.config` folder. Explain: "I need write access to your ~/.config folder to save the UniFi credentials."

### 4. Write the config file

Once directory access is granted, the mount appears at a path ending in `mnt/.config`. Use `mkdir -p` via Bash to create the subdirectory, then use the Write tool to write the file:

Target path: `<mount_root>/unifi-mcp/config.json`

Content:
```json
{
  "host": "UNIFI_HOST_VALUE",
  "api_key": "UNIFI_API_KEY_VALUE",
  "verify_ssl": false
}
```

Set `"verify_ssl": true` only if the user explicitly requested it.

Confirm the file path after writing.

### 5. Tell the user to restart Claude

Instruct: **Quit Claude completely (Cmd+Q on Mac) and relaunch.**

On first start after restart, the MCP server automatically installs Python dependencies. This takes ~10–30 seconds on first run only. Subsequent starts are instant.

### 6. Verify after restart

After the user confirms they've restarted, call the `get_application_info` MCP tool to confirm the server is connected and the controller responds. Report the result.

## Security Notes

- Credentials live only in `~/.config/unifi-mcp/config.json` on the user's local machine.
- Never passed as environment variables or stored in the plugin directory.
- API key stored in plaintext — standard practice for local MCP servers (same model as Claude Desktop's env block).
- Never display the full API key after saving.
