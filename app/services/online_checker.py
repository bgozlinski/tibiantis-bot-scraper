import httpx
from bs4 import BeautifulSoup
from typing import List
from sqlalchemy.orm import Session
from app.models.blacklist import BlacklistEntry as BlacklistModel
from datetime import datetime, timezone
from app.models.character import Character as CharacterModel
from app.models.bedmage_timer import BedmageTimer as TimerModel



class OnlineChecker:
    def __init__(self):
        self.base_url = "https://www.tibiantis.online/"

    async def get_characters_online_list(self, client: httpx.AsyncClient) -> List[str]:
        try:
            characters_online_list = f"{self.base_url}?page=whoisonline&world=2"
            response = await client.get(characters_online_list, headers={"User-Agent": "TibiantisBot/1.0"})
            online_names = []
            if soup := BeautifulSoup(response.text, "html.parser"):
                rows = soup.find_all("tr",  class_="hover")

                for row in rows:
                    columns = row.find_all("td")
                    name = columns[0].text.strip()
                    online_names.append(name)

                return online_names
            return []

        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch online list: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    async def update_online_status(self, db: Session, client: httpx.AsyncClient):
        online_names = await self.get_characters_online_list(client)

        db_blacklist = db.query(BlacklistModel).all()

        for entry in db_blacklist:
            entry.is_online = entry.character_name in online_names

        db.commit()
