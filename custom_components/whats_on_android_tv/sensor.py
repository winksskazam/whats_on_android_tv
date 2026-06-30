"""What's On Android TV."""

from __future__ import annotations

from .const import DOMAIN
from .coordinator import WhatsOnAndroidTVCoordinator


async def async_setup(hass, config):
    """Set up the integration."""
    return True


async def async_setup_entry(hass, entry):
    """Set up from a config entry."""

    coordinator = WhatsOnAndroidTVCoordinator(hass, entry)

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        ["sensor"],
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        ["sensor"],
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok