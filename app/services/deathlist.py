import httpx
from sqlalchemy.orm import Session
from app.services.discord_notifer import DiscordNotifier
from app.services.scraper import Scraper
from app.models.deathlist import DeathlistEntry
from datetime import datetime, timezone
from app.core.config import settings
from app.models.character import Character as CharacterModel
from app.services.character import CharacterService

class DeathlistService:
    @staticmethod
    async def get_recent_deaths(client: httpx.AsyncClient):
        scraper = Scraper()
        death_list_data = await scraper.get_death_list(client=client, server_id=2, page=1)

        if death_list_data:
            return death_list_data
        else:
            raise ValueError("No death list data found")

    @staticmethod
    async def save_death(db: Session, death_data: dict) -> DeathlistEntry | None:
        try:
            death_time = datetime.strptime(death_data["death_time"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except (ValueError, KeyError):
            print(f"Invalid death data format: {death_data.get('death_time')}")
            return None

        existing = db.query(DeathlistEntry).filter(
            DeathlistEntry.character_name == death_data["character_name"],
            DeathlistEntry.death_time == death_time
        ).first()

        if existing:
            return None

        entry = DeathlistEntry(
            character_name=death_data["character_name"],
            death_level=death_data["death_level"],
            death_time=death_time,
            death_by=death_data["death_by"]
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    async def get_deaths_above_level(db: Session, min_level: int):
        return db.query(DeathlistEntry).filter(DeathlistEntry.death_level >= min_level).all()

    @staticmethod
    async def check_and_notify_deaths(db: Session, client: httpx.AsyncClient):
        try:
            deaths = await DeathlistService.get_recent_deaths(client)
        except ValueError as e:
            print(f"Failed to fetch death list: {e}")
            return

        for death in deaths:
            if death.get("death_level", 0) <= settings.MIN_LEVEL_TO_CHECK_DEATH:
                continue

            character_exists = db.query(CharacterModel).filter(
                CharacterModel.name == death["character_name"]
            ).first()

            if not character_exists:
                try:
                    await CharacterService.scrape_and_save_character(death["character_name"], db, client)
                except Exception as e:
                    print(f"Failed to scrape character {death['character_name']}: {e}")
                    continue

            saved = await DeathlistService.save_death(db, death)

            if saved:
                await DiscordNotifier.send_death_embed(death, client)

