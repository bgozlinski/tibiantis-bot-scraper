import httpx
from app.core.config import settings
from datetime import datetime, timezone
from urllib.parse import quote_plus

class DiscordNotifier:
    @staticmethod
    async def send_message(message: str, client: httpx.AsyncClient):
        if not settings.DISCORD_WEBHOOK_URL:
            print("Discord Webhook URL not configured. Skipping notification.")
            return

        payload = {"content": message}

        try:
            response = await client.post(settings.DISCORD_WEBHOOK_URL, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Failed to send message to Discord: {e}")

    @staticmethod
    async def send_death_embed(death: dict, client: httpx.AsyncClient):
        webhook_url = settings.DISCORD_DEATHS_WEBHOOK_URL or settings.DISCORD_WEBHOOK_URL
        if not webhook_url:
            print("Discord Webhook URL not configured. Skipping death notification.")
            return

        character_name = death["character_name"]
        death_level = death["death_level"]
        death_by = death["death_by"]
        death_time_str = death["death_time"]  #"2026-03-15 14:30:00"

        try:
            death_time_dt = datetime.strptime(death_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
            seconds_ago = int((datetime.now(timezone.utc) - death_time_dt).total_seconds())
            time_ago_str = f"({seconds_ago}s ago)"
        except ValueError:
            death_time_dt = None
            time_ago_str = ""
            print(f"Invalid death time format: {death_time_str}")

        character_url = f"https://www.tibiantis.online/?page=character&name={quote_plus(character_name)}"

        payload = {
            "embeds": [{
                "title": character_name,
                "url": character_url,
                "color": 0xFF0000,
                "description": (
                    f"Died at level **{death_level}**\n"
                    f"{death_time_str} {time_ago_str}\n"
                    f"Killed by: {death_by}"
                )
            }]
        }

        try:
            response = await client.post(webhook_url, json=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            print(f"Failed to send death embed to Discord: {e}")