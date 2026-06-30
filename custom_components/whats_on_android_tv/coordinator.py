"""Coordinator for What's On Android TV."""

from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class WhatsOnAndroidTVCoordinator(DataUpdateCoordinator):
    """Coordinator for What's On Android TV."""

    def __init__(self, hass, config_entry):
        """Initialize coordinator."""
        self.config_entry = config_entry

        super().__init__(
            hass,
            _LOGGER,
            name="What's On Android TV",
            update_interval=timedelta(seconds=5),
        )

    async def _async_update_data(self):
        """Fetch latest data from the selected media player."""

        entity_id = self.config_entry.data["media_player"]

        state = self.hass.states.get(entity_id)

        if state is None:
            _LOGGER.warning("Media player %s not found", entity_id)
            return {}

        attributes = dict(state.attributes)

        data = {
            "state": state.state,
            "app_name": attributes.get("app_name"),
            "app_id": attributes.get("app_id"),
            "source": attributes.get("source"),
            "friendly_name": state.name,
        }

        # Include all media_player attributes so they're available on the sensor.
        data.update(attributes)

        _LOGGER.debug("Coordinator data: %s", data)
        _LOGGER.warning("Android TV attributes: %s", attributes)

        return data