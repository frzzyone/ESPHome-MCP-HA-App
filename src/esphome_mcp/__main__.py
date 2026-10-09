import asyncio
import json
import logging
import os
import time

from esphome_mcp.client import get_client
from esphome_mcp.server import mcp

LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"

logger = logging.getLogger(__name__)


def _load_options_file() -> None:
    """Load configuration from Home Assistant's /data/options.json if present."""
    options_path = os.environ.get("HA_OPTIONS_PATH", "/data/options.json")
    if os.path.isfile(options_path):
        try:
            with open(options_path, encoding="utf-8") as f:
                data = json.load(f)
            for k, v in data.items():
                if v is not None and v != "":
                    os.environ.setdefault(k.upper(), str(v))
        except Exception as e:
            logger.warning("Could not read Home Assistant options from %s: %s", options_path, e)


def _configure_logging() -> None:
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(format=LOG_FORMAT, level=getattr(logging, level, logging.INFO))


def _check_connectivity() -> None:
    """Verify connectivity to the ESPHome dashboard, retrying on failure.

    Uses the cheap REST ``/version`` endpoint so the pre-flight check does not open
    (and leave dangling) a WebSocket on a throwaway event loop — the persistent WS
    connection is established lazily within the server's own loop on first tool call.
    """
    max_retries = int(os.environ.get("ESPHOME_CONNECT_RETRIES", "12"))
    retry_delay = int(os.environ.get("ESPHOME_CONNECT_RETRY_DELAY", "5"))

    for attempt in range(1, max_retries + 1):
        try:
            version = asyncio.run(get_client().get_version())
            logger.info("Connected to ESPHome dashboard (ESPHome %s)", version)
            return
        except Exception as e:
            logger.error(
                "Failed to connect to ESPHome dashboard (attempt %d/%d): %s",
                attempt,
                max_retries,
                e,
            )
            if attempt < max_retries:
                logger.info("Retrying in %d seconds...", retry_delay)
                time.sleep(retry_delay)
    raise SystemExit(1)


def main() -> None:
    _load_options_file()
    _configure_logging()
    _check_connectivity()
    mcp.run()


def main_web() -> None:
    _load_options_file()
    _configure_logging()
    _check_connectivity()
    # stateless_http: a gateway like MetaMCP opens a NEW MCP session per burst of calls
    # and never sends DELETE /mcp, and fastmcp 3.4.x only evicts a session once its
    # server task ends — so in stateful mode every session ever served stays resident
    # (measured at ~57 KB each on a sibling wrapper, which reached 1 GB in two weeks).
    # None of the tools here use Context, progress or server-initiated notifications, so
    # sessions buy nothing. Stateless drops GET /mcp (405), which MCP clients handle per
    # spec as "this server offers no SSE stream".
    port = int(os.environ.get("PORT", "8080"))
    mcp.run(transport="http", host="0.0.0.0", port=port, stateless_http=True)


if __name__ == "__main__":
    main()
