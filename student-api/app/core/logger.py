import logging

from app.core.config import settings


def configure_logging():
    # Configure the root logger once for the whole application.
    log_level = settings.LOG_LEVEL.upper()

    logging.basicConfig(
        level=getattr(logging, log_level, logging.INFO),
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
