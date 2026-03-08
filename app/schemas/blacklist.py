from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasPath, field_validator


class BlacklistBase(BaseModel):
    character_name: str
    is_active: bool = True
    notes: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class BlacklistCreate(BaseModel):
    character_name: str
    notes: Optional[str] = None


class BlacklistUpdate(BaseModel):
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class BlacklistResponse(BlacklistBase):
    id: int
    added_at: datetime
