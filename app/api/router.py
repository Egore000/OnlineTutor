from fastapi import APIRouter, FastAPI

from app.api.root import router as root_router
from app.api.v1 import router as v1_router
from app.shared.config import settings

# Роутер, отвечающий за версионирование API
router = APIRouter(prefix=settings.api.prefix)
router.include_router(v1_router)


def configure_routes(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(router)
