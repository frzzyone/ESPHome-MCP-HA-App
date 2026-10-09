# ESPHome MCP for Home Assistant OS

The **ESPHome MCP** app runs a Model Context Protocol (MCP) server directly inside Home Assistant OS. It connects to your ESPHome Device Builder dashboard over WebSocket and exposes high-level tools to AI assistants (such as Claude Desktop, Cursor, Goose, etc.) to list devices, inspect and edit YAML configurations, validate configurations, read live logs, and trigger firmware compilation and OTA flashing.

---

## 🚀 Getting Started

### 1. Prerequisites

Before starting this app, ensure you have an ESPHome dashboard running:
- **Official ESPHome Add-on**: If you are using the official ESPHome add-on in Home Assistant OS, ESPHome MCP can connect directly across the internal Docker network.
- **External ESPHome Dashboard**: If your dashboard runs on another machine or container, ensure it is network-accessible.

### 2. Configuration Options

In the **Configuration** tab of this app:

| Option | Type | Default | Description |
|---|---|---|---|
| `esphome_dashboard_url` | string | `http://5c53de3a-esphome:6052` | URL of the ESPHome dashboard. For the official ESPHome add-on running on Home Assistant OS, use `http://5c53de3a-esphome:6052`. For external dashboards, enter the full URL (e.g. `http://192.168.1.100:6052` or `https://esphome.example.com`). |
| `esphome_dashboard_username` | string | `""` | Dashboard username (only required if your ESPHome dashboard has Basic Auth enabled). |
| `esphome_dashboard_password` | password | `""` | Dashboard password (only required if your ESPHome dashboard has Basic Auth enabled). |
| `log_level` | string | `INFO` | Verbosity of server logs: `DEBUG`, `INFO`, `WARNING`, or `ERROR`. |

### 3. Network Port

By default, the app exposes port **8080** for Streamable HTTP MCP connections. You can change the host port in the **Network** card on the app's Info tab if port 8080 is already used on your Home Assistant host.

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

### Cannot connect to ESPHome dashboard
1. Ensure the ESPHome add-on is started and healthy.
2. If using the official ESPHome add-on, verify `esphome_dashboard_url` is set to `http://5c53de3a-esphome:6052`.
3. If your ESPHome add-on has authentication turned on, make sure both `esphome_dashboard_username` and `esphome_dashboard_password` are filled in.
4. Check the **Log** tab of this app for connection error details.
