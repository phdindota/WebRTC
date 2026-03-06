"""Diagnostics support for WebRTC Camera."""
from __future__ import annotations

import platform
from typing import Any
from urllib.parse import urlparse

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import MAJOR_VERSION, MINOR_VERSION
from homeassistant.core import HomeAssistant

from .utils import DOMAIN, Server, BINARY_VERSION, get_arch
from . import LINKS


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    server = hass.data.get(DOMAIN)

    is_local_server = isinstance(server, Server)

    data = {
        "go2rtc_binary_version": BINARY_VERSION,
        "go2rtc_mode": "local_binary" if is_local_server else "external_url",
        "go2rtc_available": server.available if is_local_server else True,
        "platform": {
            "system": platform.system(),
            "machine": platform.machine(),
            "arch": get_arch() or "unsupported",
        },
        "active_links": len(LINKS),
        "ha_version": f"{MAJOR_VERSION}.{MINOR_VERSION}",
    }

    # Don't include sensitive URLs
    if not is_local_server and server:
        parsed = urlparse(server)
        data["go2rtc_host"] = parsed.hostname
        data["go2rtc_port"] = parsed.port

    return data
