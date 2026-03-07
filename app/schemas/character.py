from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, AliasPath, field_validator


class Character(BaseModel):
    name: str = Field(validation_alias="name")
    sex: str = Field(validation_alias="sex")
    vocation: Optional[str] = Field(None, validation_alias="vocation")
    level: int = Field(validation_alias="level")
    world: str = Field(validation_alias="world")
    residence: str = Field(validation_alias="residence")
    house: Optional[str] = Field(None, validation_alias="house")
    guild: Optional[str] = Field(None, validation_alias="guild")
    last_login: Optional[datetime] = Field(None, validation_alias="last login")
    account_status: str = Field(validation_alias="account status")

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("last_login", mode="before")
    @classmethod
    def convert_last_login(cls, v):
        if isinstance(v, str):
            clean_date = v.replace(" CE", "").strip()
            try:
                return datetime.strptime(clean_date, "%d %b %Y %H:%M:%S")
            except ValueError:
                return None
        return v


class CharacterCreate(Character):
    pass


class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    sex: Optional[str] = None
    vocation: Optional[str] = None
    level: Optional[int] = None
    world: Optional[str] = None
    residence: Optional[str] = None
    house: Optional[str] = None
    guild: Optional[str] = None
    last_login: Optional[datetime] = None
    account_status: Optional[str] = None


class CharacterResponse(Character):
    pass