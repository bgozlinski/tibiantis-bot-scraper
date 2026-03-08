from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.core.database import get_db
from app.dependencies import get_http_client
from app.services.blacklist import BlacklistService
from app.schemas.blacklist import BlacklistResponse, BlacklistCreate
from app.services.online_checker import OnlineChecker
from app.models.blacklist import BlacklistEntry as BlacklistModel
from typing import List

router = APIRouter(prefix="/blacklist", tags=["blacklist"])

@router.get("/", response_model=List[BlacklistResponse])
async def get_blacklist(db: Session = Depends(get_db)):
    return BlacklistService.get_blacklist(db)

@router.post("/{name}", response_model=BlacklistResponse)
async def add_to_blacklist(
        name: str,
        db: Session = Depends(get_db),
        client: httpx.AsyncClient = Depends(get_http_client)
):
    try:
        return await BlacklistService.add_to_blacklist(db, BlacklistCreate(character_name=name), client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{entry_id}")
async def remove_from_blacklist(entry_id: int, db: Session = Depends(get_db)):
    success = BlacklistService.remove_from_blacklist(db, entry_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"status": "deleted"}

@router.get("/online", response_model=List[BlacklistResponse])
async def get_online_blacklisted(
        db: Session = Depends(get_db),
        client: httpx.AsyncClient = Depends(get_http_client)
):
    blacklist_online_check = OnlineChecker()
    await blacklist_online_check.update_online_status(db, client)

    return db.query(BlacklistModel).filter(BlacklistModel.is_online == True).all()