from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.core.database import get_db
from app.dependencies import get_http_client
from app.services.bedmage_timer import BedmageTimerService
from app.schemas.bedmage_timer import BedmageTimerResponse, BedmageTimerCreate
from app.services.online_checker import OnlineChecker
from app.models.bedmage_timer import BedmageTimer as BedmageTimerModel
from typing import List

router = APIRouter(prefix="/bedmage_timers", tags=["bedmage_timers"])

@router.get("/", response_model=List[BedmageTimerResponse])
async def get_timers(db: Session = Depends(get_db)):
    return BedmageTimerService.get_all_timers(db)

@router.post("/", response_model=BedmageTimerResponse)
async def add_timer(
        timer_data: BedmageTimerCreate,
        db: Session = Depends(get_db),
        client: httpx.AsyncClient = Depends(get_http_client),
):
    try:
        return await BedmageTimerService.create_timer(db, timer_data, client)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{timer_id}")
async def delete_timer(timer_id: int, db: Session = Depends(get_db)):
    success = BedmageTimerService.delete_timer(db, timer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entry not found")
    return {"status": "deleted"}
