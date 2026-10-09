#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting ESPHome MCP Server for Home Assistant OS"
echo "=========================================================="

OPTIONS_FILE="/data/options.json"

if [ -f "$OPTIONS_FILE" ]; then
    echo "[INFO] Loading configuration from ${OPTIONS_FILE}..."

    # Extract configuration using python
    DASHBOARD_URL=$(python3 -c "import json; conf=json.load(open('${OPTIONS_FILE}')); print(conf.get('esphome_dashboard_url') or '')")
    USERNAME=$(python3 -c "import json; conf=json.load(open('${OPTIONS_FILE}')); print(conf.get('esphome_dashboard_username') or '')")
    PASSWORD=$(python3 -c "import json; conf=json.load(open('${OPTIONS_FILE}')); print(conf.get('esphome_dashboard_password') or '')")
    LOG_LVL=$(python3 -c "import json; conf=json.load(open('${OPTIONS_FILE}')); print(conf.get('log_level') or 'INFO')")

    if [ -n "$DASHBOARD_URL" ]; then
        export ESPHOME_DASHBOARD_URL="$DASHBOARD_URL"
    fi
    if [ -n "$USERNAME" ]; then
        export ESPHOME_DASHBOARD_USERNAME="$USERNAME"
    fi
    if [ -n "$PASSWORD" ]; then
        export ESPHOME_DASHBOARD_PASSWORD="$PASSWORD"
    fi
    if [ -n "$LOG_LVL" ]; then
        export LOG_LEVEL="$LOG_LVL"
    fi
fi

if [ -z "$ESPHOME_DASHBOARD_URL" ]; then
    echo "[WARN] ESPHOME_DASHBOARD_URL not set! Falling back to default: http://5c53de3a-esphome:6052"
    export ESPHOME_DASHBOARD_URL="http://5c53de3a-esphome:6052"
fi

echo "[INFO] ESPHome Dashboard URL: ${ESPHOME_DASHBOARD_URL}"
if [ -n "$ESPHOME_DASHBOARD_USERNAME" ]; then
    echo "[INFO] Authentication: enabled for user '${ESPHOME_DASHBOARD_USERNAME}'"
else
    echo "[INFO] Authentication: disabled"
fi
echo "[INFO] Log Level: ${LOG_LEVEL:-INFO}"
echo "[INFO] Listening for MCP client connections on port 8080..."
echo "=========================================================="

exec esphome-mcp-web
