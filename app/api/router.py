from fastapi import APIRouter, FastAPI

from app.api.root import router as root_router
from app.api.v1 import router as v1_router
from app.shared.config import APISettings

settings = APISettings()


# Роутер, отвечающий за версионирование API
router = APIRouter(prefix=settings.prefix)
router.include_router(v1_router)


def configure_routes(app: FastAPI) -> None:
    app.include_router(root_router)
    app.include_router(router)
