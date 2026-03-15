from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DeathlistBase(BaseModel):
    character_name: str
    death_level: int
    death_time: datetime
    death_by: str

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class DeathlistResponse(DeathlistBase):
    id: int
