"""Sensor platform for What's On Android TV."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import WhatsOnAndroidTVCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor."""

    _LOGGER.warning("What's On Android TV: async_setup_entry called")

    coordinator: WhatsOnAndroidTVCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensor = WhatsOnAndroidTVSensor(coordinator, entry)

    _LOGGER.warning("What's On Android TV: adding sensor entity")

    async_add_entities([sensor])


class WhatsOnAndroidTVSensor(
    CoordinatorEntity[WhatsOnAndroidTVCoordinator],
    SensorEntity,
):
    """Representation of the current Android TV app."""

    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: WhatsOnAndroidTVCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._attr_unique_id = f"{entry.entry_id}_current_app"
        self._attr_name = "Current App"
        self._attr_icon = "mdi:android-tv"

        _LOGGER.warning("What's On Android TV: sensor initialized")

    @property
    def native_value(self):
        """Return the current app."""
        return self.coordinator.data.get("app_name")

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return self.coordinator.data