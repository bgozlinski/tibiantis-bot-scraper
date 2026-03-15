from app.core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint


class DeathlistEntry(Base):
    __tablename__ = "deathlist"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    character_name = Column(String, ForeignKey("characters.name", ondelete="CASCADE"), nullable=False)
    death_level = Column(Integer, nullable=False)
    death_time = Column(DateTime(timezone=True), nullable=False)
    death_by = Column(String, nullable=False)

    __table_args__ = (
        UniqueConstraint("character_name", "death_time", name="uq_death_character_time"),
    )
