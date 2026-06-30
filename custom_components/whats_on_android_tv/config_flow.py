"""Config flow for What's On Android TV."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import DOMAIN


class WhatsOnAndroidTVConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    """Handle config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle setup."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["media_player"],
                data=user_input,
            )

        media_players = {}

        for entity_id, state in self.hass.states.async_all("media_player"):
            media_players[entity_id] = state.name

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("media_player"): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=[
                                selector.SelectOptionDict(
                                    value=eid,
                                    label=name,
                                )
                                for eid, name in sorted(media_players.items())
                            ]
                        )
                    )
                }
            ),
        )