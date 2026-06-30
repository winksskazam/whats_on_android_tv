"""Sensor platform for What's On Android TV."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .app_database import APP_DATABASE
from .const import DOMAIN
from .coordinator import WhatsOnAndroidTVCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor."""

    coordinator: WhatsOnAndroidTVCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            WhatsOnAndroidTVSensor(
                coordinator,
                entry,
            )
        ]
    )


class WhatsOnAndroidTVSensor(
    CoordinatorEntity[WhatsOnAndroidTVCoordinator],
    SensorEntity,
):
    """Current Android TV application."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:android-tv"

    def __init__(
        self,
        coordinator: WhatsOnAndroidTVCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_current_app"
        self._attr_name = "Current App"

    @property
    def native_value(self):
        """Return the friendly application name."""

        package = (
            self.coordinator.data.get("app_id")
            or self.coordinator.data.get("app_name")
            or self.coordinator.data.get("source")
        )

        if not package:
            return None

        app = APP_DATABASE.get(package)

        if app:
            return app["name"]

        return package

    @property
    def extra_state_attributes(self):
        """Return extra attributes."""

        package = (
            self.coordinator.data.get("app_id")
            or self.coordinator.data.get("app_name")
            or self.coordinator.data.get("source")
        )

        app = APP_DATABASE.get(package, {})

        return {
            **self.coordinator.data,
            "package": package,
            "friendly_app_name": app.get("name"),
            "category": app.get("category"),
            "icon_file": app.get("icon"),
        }