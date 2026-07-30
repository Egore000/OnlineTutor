from fastapi import APIRouter, FastAPI

from app.api.v1 import router
from app.shared.config import settings

base_router = APIRouter(prefix=settings.api.prefix)
base_router.include_router(router)


def configure_routes(app: FastAPI) -> None:
    app.include_router(base_router)
