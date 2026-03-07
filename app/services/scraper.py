import httpx
from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional
import asyncio

class Scraper:
    def __init__(self):
        self.base_url = "https://www.tibiantis.online/"
        self.session = httpx.AsyncClient()

    async def get_character_data(self, character_name: str) -> Optional[Dict]:
        try:
            character_data = {}
            character_url = f"{self.base_url}?page=character&name={character_name}"
            response = await self.session.get(character_url)

            if soup := BeautifulSoup(response.text, "html.parser"):
                rows = soup.find_all("tr",  class_="hover")

                if not rows:
                    return None

                for row in rows:
                    columns = row.find_all("td")
                    key = columns[0].text.strip().lower().rstrip(':')
                    value = columns[1].text.strip()
                    character_data[key] = value

                return character_data
            else:
                return None

        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch character data: {e}")
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


async def main():
    scraper = Scraper()
    character_data = await scraper.get_character_data("Yhral")
    print(character_data)
    await scraper.session.aclose()

if __name__ == "__main__":
    asyncio.run(main())
