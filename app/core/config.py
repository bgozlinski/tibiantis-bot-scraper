"""Configuration settings for the Services.
"""

from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = "5432"
    DB_NAME: str

    PROJECT_NAME: str = "Tibiantis Bot Scrapper"
    API_V1_PREFIX: str = "/api/v1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DISCORD_WEBHOOK_URL: str = ""
    DISCORD_DEATHS_WEBHOOK_URL: str = ""

    SCHEDULER_TIMER_MINUTES: int = 5
    MIN_LEVEL_TO_CHECK_DEATH: int = 30


    model_config = ConfigDict(env_file=".env", case_sensitive=True)

    @property
    def DATABASE_URL(self) -> str:
        """Construct PostgreSQL connection URL.
        
        Returns:
            str: Full database connection string.
        """
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
