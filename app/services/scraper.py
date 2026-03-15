import httpx
from bs4 import BeautifulSoup
from typing import Optional
from app.schemas.character import CharacterCreate
import asyncio


class Scraper:
    def __init__(self):
        self.tibantis_online_base_url = "https://www.tibiantis.online/"
        self.tibiantis_info_base_url = "https://tibiantis.info/"
        self.headers = {"User-Agent": "TibiantisBot/1.0"}

    async def get_character_data(
            self,
            character_name: str,
            client: httpx.AsyncClient
    ) -> Optional[CharacterCreate]:
        try:
            character_url = f"{self.tibantis_online_base_url}?page=character&name={character_name}"
            response = await client.get(character_url, headers=self.headers)

            if soup := BeautifulSoup(response.text, "html.parser"):
                rows = soup.find_all("tr",  class_="hover")

                if not rows:
                    return None

                character_dict = {}
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) < 2:
                        continue
                    key = columns[0].text.strip().lower().rstrip(':')
                    value = columns[1].text.strip()
                    character_dict[key] = value
                return CharacterCreate.model_validate(character_dict)
            else:
                return None

        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch character data: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    async def set_server(self, client: httpx.AsyncClient, server_id: int) -> None:
        """
        1 = Ancestra
        2 = Concordia
        """
        try:
            server_url = f"{self.tibiantis_info_base_url}index/server/tibiantis/{server_id}"
            response = await client.get(server_url, headers=self.headers)

            if response.status_code not in (200, 302):
                raise Exception(f"Unexpected status code while setting server: {response.status_code}")

        except httpx.HTTPError as e:
            raise Exception(f"Failed to set server {server_id}: {e}") from e

    async def get_death_list(
            self,
            client: httpx.AsyncClient,
            server_id: int = 2,
            page: int = 1
    ) -> list[dict]:

        try:
            deaths = []
            await self.set_server(client, server_id)
            death_list_url = f"{self.tibiantis_info_base_url}stats/deaths/{page}"
            response = await client.get(death_list_url, headers=self.headers)

            if soup := BeautifulSoup(response.text, "html.parser"):
                table = soup.find("table", class_="mytab long")
                if not table:
                    return []

                rows = table.find_all("tr")[1:]  # pomijamy header


                for row in rows:
                    columns = (row.find_all("td"))
                    if len(columns) < 4:
                        continue

                    name = columns[0].get_text(" ", strip=True).rsplit("(", 1)[0].strip()
                    death_level = columns[0].get_text(" ", strip=True).rsplit("(", 1)[1].strip(")")
                    date = columns[2].get_text(strip=True)
                    killed_by = columns[3].get_text(" ", strip=True)

                    deaths_dict = {
                        "character_name": name,
                        "death_level": int(death_level),
                        "death_time": date,
                        "death_by": killed_by
                    }
                    deaths.append(deaths_dict)

            return deaths

        except Exception as e:
            raise Exception(f"An error occurred: {e}")
