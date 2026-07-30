from fastapi import APIRouter, FastAPI

from app.api.v1 import router

base_router = APIRouter(prefix="/api")
base_router.include_router(router)


def configure_routes(app: FastAPI) -> None:
    app.include_router(base_router)
