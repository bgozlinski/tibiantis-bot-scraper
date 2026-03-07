from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, unique=True, nullable=False)
    sex = Column(String, nullable=True)
    vocation = Column(String, nullable=True)
    level = Column(Integer, nullable=True)
    world = Column(String, nullable=True)
    residence = Column(String, nullable=True)
    house = Column(String, nullable=True)
    guild = Column(String, nullable=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    account_status = Column(String, nullable=True)


