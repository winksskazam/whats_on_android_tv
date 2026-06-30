"""Sensor platform for What's On Android TV."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .app_names import APP_DATABASE
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
        [WhatsOnAndroidTVSensor(coordinator, entry)],
        True,
    )


class WhatsOnAndroidTVSensor(
    CoordinatorEntity[WhatsOnAndroidTVCoordinator],
    SensorEntity,
):
    """Current Android TV application."""

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

    @property
    def native_value(self):
        """Return the friendly application name."""

        package = self.coordinator.data.get("app_name")

        if not package:
            return None

        app = APP_DATABASE.get(package)

        if app:
            return app["name"]

        return package

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""

        attributes = dict(self.coordinator.data)

        package = self.coordinator.data.get("app_name")
        app = APP_DATABASE.get(package)

        if app:
            attributes["friendly_app_name"] = app["name"]
            attributes["category"] = app["category"]
            attributes["icon_file"] = app["icon"]

        return attributes
    
    @property
    def entity_picture(self):
        """Return the icon for the current app."""

        package = self.coordinator.data.get("app_name")

        if not package:
            return None

        app = APP_DATABASE.get(package)

        if not app:
            return None

        return f"/local/android_tv_icons/{app['icon']}"