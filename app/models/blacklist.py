from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey


class BlacklistEntry(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    character_name = Column(String, ForeignKey("characters.name", ondelete="CASCADE"), unique=True, nullable=False)
    added_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    is_active = Column(Boolean, default=True)
    notes = Column(String)
    is_online = Column(Boolean, default=False)


