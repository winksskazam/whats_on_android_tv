"""Config flow for What's On Android TV."""

from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import entity_registry as er
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

        entity_registry = er.async_get(self.hass)

        media_players = {}

        for state in self.hass.states.async_all("media_player"):
            entry = entity_registry.async_get(state.entity_id)

            if entry is None:
                continue

            print(state.entity_id, entry.platform)

            if entry.platform not in (
                "androidtv",
                "androidtv_remote",
            ):
                continue

            media_players[state.entity_id] = state.name

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