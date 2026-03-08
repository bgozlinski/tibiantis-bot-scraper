from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class BedmageTimerBase(BaseModel):
    character_name: str
    timer_minutes: int
    is_active: bool

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class BedmageTimerCreate(BaseModel):
    character_name: str
    timer_minutes: int


class BedmageTimerUpdate(BaseModel):
    timer_minutes: Optional[int] = None
    is_active: Optional[bool] = None


class BedmageTimerResponse(BedmageTimerBase):
    id: int
    created_at: datetime
    last_triggered_at: Optional[datetime]
