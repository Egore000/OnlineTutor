from fastapi import FastAPI

from app.core.lifespan import lifespan
from app.shared.config import settings


def create_app() -> FastAPI:
    return FastAPI(
        title=settings.app.name,
        description=settings.app.description,
        version=settings.app.version,
        debug=settings.app.debug,
        lifespan=lifespan,
    )
