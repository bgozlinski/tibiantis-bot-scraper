import httpx
from sqlalchemy.orm import Session
from app.models.bedmage_timer import BedmageTimer as TimerModel
from app.models.character import Character as CharacterModel
from app.schemas.bedmage_timer import BedmageTimerCreate
from datetime import datetime, timezone
from app.services.discord_notifer import DiscordNotifier
from app.services.character import CharacterService


class BedmageTimerService:
    @staticmethod
    async def create_timer(db: Session, data: BedmageTimerCreate, client: httpx.AsyncClient) -> TimerModel:
        db_character = db.query(CharacterModel).filter(CharacterModel.name == data.character_name).first()
        if not db_character:
            try:
                await CharacterService.scrape_and_save_character(data.character_name, db, client)
            except ValueError:
                raise ValueError(f"Character '{data.character_name}' not found on Tibiantis.")

        existing_timer = db.query(TimerModel).filter(TimerModel.character_name == data.character_name).first()
        if existing_timer:
            raise ValueError(f"Timer for {data.character_name} already exists.")

        db_timer = TimerModel(**data.model_dump())
        db.add(db_timer)
        db.commit()
        db.refresh(db_timer)
        return db_timer

    @staticmethod
    async def check_timers(db: Session, client: httpx.AsyncClient):
        db_timer = db.query(TimerModel).filter(TimerModel.is_active == True).all()
        for timer in db_timer:
            try:
                await CharacterService.scrape_and_save_character(timer.character_name, db, client)
            except Exception as e:
                print(f"Error scraping character {timer.character_name}: {e}")
                continue
            character = db.query(CharacterModel).filter(CharacterModel.name == timer.character_name).first()

            if character and character.last_login:
                diff = datetime.now(timezone.utc) - character.last_login
                diff_minutes = diff.total_seconds() / 60

                is_time_up = diff_minutes >= timer.timer_minutes
                not_triggered_yet = (timer.last_triggered_at is None or timer.last_triggered_at < character.last_login)

                if is_time_up and not_triggered_yet:
                    msg = f"🔔 Postać {timer.character_name} jest wylogowana od {int(diff_minutes)} minut!"
                    await DiscordNotifier.send_message(msg, client)

                    timer.last_triggered_at = datetime.now(timezone.utc)
                    db.commit()

    @staticmethod
    def get_all_timers(db: Session):
        return db.query(TimerModel).all()

    @staticmethod
    def delete_timer(db: Session, timer_id: int) -> bool:
        db_timer = db.query(TimerModel).filter(TimerModel.id == timer_id).first()
        if db_timer:
            db.delete(db_timer)
            db.commit()
            return True
        return False
