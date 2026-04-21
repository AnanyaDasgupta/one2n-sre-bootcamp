import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Application settings
    PORT: int = int(os.getenv("PORT", 8000))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")

    # Database (we'll use this in next step)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

# Create a single settings instance to use across the app
settings = Settings()