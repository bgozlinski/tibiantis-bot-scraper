import httpx
from app.core.config import settings

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