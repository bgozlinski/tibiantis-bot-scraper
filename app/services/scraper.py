import httpx
from bs4 import BeautifulSoup
from typing import Optional
from app.schemas.character import CharacterCreate


class Scraper:
    def __init__(self):
        self.base_url = "https://www.tibiantis.online/"

    async def get_character_data(self, character_name: str, client: httpx.AsyncClient) -> Optional[CharacterCreate]:
        try:
            character_url = f"{self.base_url}?page=character&name={character_name}"
            response = await client.get(character_url, headers={"User-Agent": "TibiantisBot/1.0"})

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
                print(character_dict)
                return CharacterCreate.model_validate(character_dict)
            else:
                return None

        except httpx.HTTPError as e:
            raise Exception(f"Failed to fetch character data: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

