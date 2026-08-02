import logging

from app.shared.config import LoggingSettings, settings
from app.shared.logging.formatters import formatter

log_settings = LoggingSettings()


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("app")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.setLevel(log_settings.level)

    if settings.mode == "TEST":
        logger.setLevel(logging.ERROR)

    return logger
