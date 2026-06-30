"""Coordinator for What's On Android TV."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class WhatsOnAndroidTVCoordinator(DataUpdateCoordinator):
    """Coordinator for What's On Android TV."""

    def __init__(self, hass, config_entry):
        """Initialize the coordinator."""
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name="What's On Android TV",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        """Fetch the latest data."""

        return {
            "selected_entity": self.config_entry.data["media_player"],
        }