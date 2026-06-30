"""Config flow for What's On Android TV."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.media_player import DOMAIN as MP_DOMAIN
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.selector import SelectSelector
from homeassistant.helpers.selector import SelectSelectorConfig
from homeassistant.helpers.selector import SelectSelectorMode

from .const import CONF_MEDIA_PLAYER
from .const import DOMAIN


class WhatsOnAndroidTVConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Select an Android TV entity."""

        registry = er.async_get(self.hass)

        media_players = []

        for entity in registry.entities.values():
            if entity.domain != MP_DOMAIN:
                continue

            media_players.append(
                {
                    "value": entity.entity_id,
                    "label": entity.original_name or entity.entity_id,
                }
            )

        media_players.sort(key=lambda x: x["label"])

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_MEDIA_PLAYER],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MEDIA_PLAYER): SelectSelector(
                        SelectSelectorConfig(
                            options=media_players,
                            mode=SelectSelectorMode.DROPDOWN,
                        )
                    )
                }
            ),
        )