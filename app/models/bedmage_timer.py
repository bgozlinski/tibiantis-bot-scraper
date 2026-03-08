from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, Boolean, ForeignKey


class BedmageTimer(Base):
    __tablename__ = "bedmage_timers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    character_name = Column(String, ForeignKey("characters.name", ondelete="CASCADE"), unique=True, nullable=False)
    timer_minutes = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)
    last_triggered_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())



