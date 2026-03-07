import httpx
from sqlalchemy.orm import Session
from app.models.character import Character as CharacterModel
from app.schemas.character import CharacterCreate
from app.services.scraper import Scraper

class CharacterService:
    @staticmethod
    async def upsert_character(db: Session, character_data: CharacterCreate) -> CharacterModel:
        db_character = db.query(CharacterModel).filter(CharacterModel.name == character_data.name).first()
        if db_character:
            for key, value in character_data.model_dump().items():
                setattr(db_character, key, value)
        else:
            db_character = CharacterModel(**character_data.model_dump())
            db.add(db_character)

        db.commit()
        db.refresh(db_character)

        return db_character

    @staticmethod
    async def scrape_and_save_character(name: str, db:Session, client: httpx.AsyncClient) -> CharacterModel:
        scraper = Scraper()
        character_data = await scraper.get_character_data(name, client)

        if character_data:
            return await CharacterService.upsert_character(db, character_data)
        else:
            raise ValueError(f"Character '{name}' not found on the website")