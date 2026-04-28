from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    # Read the database connection string from the environment or .env file.
    DATABASE_URL: str
    LOG_LEVEL: str = "INFO"
    ENV: Literal["dev", "prod"] = "dev"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


# Shared settings instance imported across the application.
settings = Settings()
