import logging

from app.shared.config import settings
from app.shared.logging.formatters import formatter


def configure_logging() -> logging.Logger:
    logger = logging.getLogger("app")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.setLevel(settings.log.level)

    if settings.app.mode == "TEST":
        logger.setLevel(logging.ERROR)

    return logger
