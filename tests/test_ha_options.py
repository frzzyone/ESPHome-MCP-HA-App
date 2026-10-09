import json
import os
from esphome_mcp.__main__ import _load_options_file


def test_load_options_file(tmp_path, monkeypatch):
    options_file = tmp_path / "options.json"
    options_data = {
        "esphome_dashboard_url": "http://5c53de3a-esphome:6052",
        "esphome_dashboard_username": "myuser",
        "esphome_dashboard_password": "secretpassword",
        "log_level": "DEBUG",
        "empty_key": "",
        "null_key": None,
    }
    options_file.write_text(json.dumps(options_data), encoding="utf-8")

    monkeypatch.setenv("HA_OPTIONS_PATH", str(options_file))
    monkeypatch.delenv("ESPHOME_DASHBOARD_URL", raising=False)
    monkeypatch.delenv("ESPHOME_DASHBOARD_USERNAME", raising=False)
    monkeypatch.delenv("ESPHOME_DASHBOARD_PASSWORD", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("EMPTY_KEY", raising=False)

    _load_options_file()

    assert os.environ.get("ESPHOME_DASHBOARD_URL") == "http://5c53de3a-esphome:6052"
    assert os.environ.get("ESPHOME_DASHBOARD_USERNAME") == "myuser"
    assert os.environ.get("ESPHOME_DASHBOARD_PASSWORD") == "secretpassword"
    assert os.environ.get("LOG_LEVEL") == "DEBUG"
    assert "EMPTY_KEY" not in os.environ
