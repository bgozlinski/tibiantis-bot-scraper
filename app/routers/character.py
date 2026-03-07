from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.core.database import get_db
from app.dependencies import get_http_client
from app.services.character import CharacterService
from app.schemas.character import CharacterResponse
from app.models.character import Character as CharacterModel

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/{name}", response_model=CharacterResponse)
async def get_character(name: str, db: Session = Depends(get_db)):
    db_character = db.query(CharacterModel).filter(CharacterModel.name == name).first()
    if not db_character:
        raise HTTPException(status_code=404, detail=f"Character '{name}' not found")
    return db_character

@router.post("/scrape/{name}", response_model=CharacterResponse)
async def scrape_character(name: str, db: Session = Depends(get_db), client: httpx.AsyncClient = Depends(get_http_client)):
    try:
        return await CharacterService.scrape_and_save_character(name, db, client)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
