# ESPHome MCP for Home Assistant OS

The **ESPHome MCP** app runs a Model Context Protocol (MCP) server directly inside Home Assistant OS. It connects to your ESPHome Device Builder dashboard over WebSocket and exposes high-level tools to AI assistants (such as Claude Desktop, Cursor, Goose, etc.) to list devices, inspect and edit YAML configurations, validate configurations, read live logs, and trigger firmware compilation and OTA flashing.

---

## 🚀 Getting Started

### 1. Prerequisites (Crucial Step!)

If you are using the official **ESPHome Add-on** in Home Assistant OS:
By default, the official ESPHome add-on runs in **Ingress-only** mode and its direct dashboard port `6052` is disabled. You must enable it so other services can connect:

1. In Home Assistant, go to **Settings** → **Add-ons** (or **Apps**) → **ESPHome**.
2. Scroll down to the **Network** card, and in the port input field for `6052/tcp`, type **`6052`**.
3. Go to the **Configuration** tab in the ESPHome add-on, and toggle ON **"Disable external authentication"** (or in YAML editor: `leave_front_door_open: true`).
4. Click **Save** and then **Restart** the ESPHome add-on.
5. *(Verification)* You should now be able to open `http://<HOME_ASSISTANT_IP>:6052` directly in your browser.

> [!IMPORTANT]
> The ESPHome Device Builder explicitly requires **"Disable external authentication"** to be turned on when port 6052 is mapped (`leave_front_door_open: true`), otherwise it will not bind port 6052 (`Public port 6052 NOT bound`).

### 2. Configuration Options

In the **Configuration** tab of the **ESPHome MCP** app:

| Option | Type | Default | Description |
|---|---|---|---|
| `esphome_dashboard_url` | string | `http://127.0.0.1:6052` | URL of the ESPHome dashboard. Because this add-on uses host networking, `http://127.0.0.1:6052` connects directly to the local ESPHome dashboard. For external dashboards on another server, specify the address (e.g. `http://192.168.1.100:6052`). |
| `esphome_dashboard_username` | string | `""` | Dashboard username (only required if your ESPHome dashboard has Basic Auth enabled). |
| `esphome_dashboard_password` | password | `""` | Dashboard password (only required if your ESPHome dashboard has Basic Auth enabled). |
| `log_level` | string | `INFO` | Verbosity of server logs: `DEBUG`, `INFO`, `WARNING`, or `ERROR`. |

---

## 🤖 Connecting MCP Clients

The app serves MCP over **Streamable HTTP** at:
```text
http://<HOME_ASSISTANT_IP>:8080/mcp
```
*(Replace `<HOME_ASSISTANT_IP>` with your Home Assistant host IP or hostname).*

### Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "esphome": {
      "type": "http",
      "url": "http://<HOME_ASSISTANT_IP>:8080/mcp"
    }
  }
}
```

### Cursor / Windsurf / Cline

In your MCP settings, add an HTTP / SSE server:
- **Name**: `esphome`
- **Type**: `Streamable HTTP / SSE`
- **URL**: `http://<HOME_ASSISTANT_IP>:8080/mcp`

---

## 🛠️ Available MCP Tools

| Tool | Description |
|---|---|
| `list_devices` / `list_device_names` | Inventory configured ESPHome devices and metadata |
| `check_device_update` | Check if a firmware update is available for a device |
| `get_device_status` | Query online/offline status and IP/mDNS address |
| `get_device_version` | Compare deployed firmware version with current ESPHome version |
| `get_device_configuration` | Read raw device YAML configuration |
| `edit_device_configuration` | Modify device YAML configuration with automatic post-validation |
| `validate_device_configuration` | Full ESPHome compiler schema validation without saving |
| `migrate_device_configuration` | Respell legacy YAML keys for updated ESPHome versions |
| `search_device_configurations` | Search across all device configurations for matching strings |
| `get_device_logs` | Stream live or recent logs from a device |
| `troubleshoot_device` | Run network connectivity diagnostic probes (DNS, mDNS, ping) |
| `decode_device_backtrace` | Decode crash backtraces into source file locations |
| `get_esphome_schema` | Inspect ESPHome component schema |
| `install_device_configuration` | Compile and flash firmware via OTA |
| `update_device` | Recompile and flash latest firmware via OTA |

---

## 🔍 Troubleshooting

### Error: `Failed to connect to ESPHome dashboard: All connection attempts failed`
1. **Did you enable port 6052 in the ESPHome add-on?** Go to Home Assistant → Settings → Add-ons → ESPHome → Network card → enter `6052` into `6052/tcp` → click Save → restart ESPHome.
2. **What URL are you using?**
   - Use `http://127.0.0.1:6052` (recommended).
   - Do **not** use `http://5c53de3a-esphome:6052` or `http://5c53de3b-esphome:6052` because the official ESPHome add-on runs with host networking and has no Docker bridge DNS entry.
3. Test accessing `http://<HOME_ASSISTANT_IP>:6052` in your web browser from your PC/phone. If it doesn't open the ESPHome dashboard, port 6052 is not yet listening.
