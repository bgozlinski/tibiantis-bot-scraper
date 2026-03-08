import httpx
from pygments.lexers import data
from sqlalchemy.orm import Session
from app.models.blacklist import BlacklistEntry as BlacklistModel
from app.models.character import Character as CharacterModel
from app.schemas.blacklist import BlacklistCreate
from app.services.character import CharacterService

class BlacklistService:
    @staticmethod
    async def add_to_blacklist(db: Session, data: BlacklistCreate, client: httpx.AsyncClient) -> BlacklistModel:
        char_exists = db.query(CharacterModel).filter(CharacterModel.name == data.character_name).first()
        if not char_exists :
            await CharacterService.scrape_and_save_character(data.character_name, db, client)

        existing_entry = db.query(BlacklistModel).filter(BlacklistModel.character_name == data.character_name).first()
        if existing_entry:
            return existing_entry

        new_entry = BlacklistModel(**data.model_dump())
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)
        return new_entry

    @staticmethod
    def get_blacklist(db: Session) -> list[BlacklistModel]:
        return db.query(BlacklistModel).all()

    @staticmethod
    def remove_from_blacklist(db: Session, entry_id: int) -> bool:
        entry = db.query(BlacklistModel).filter(BlacklistModel.id == entry_id).first()
        if entry:
            db.delete(entry)
            db.commit()
            return True
        return False