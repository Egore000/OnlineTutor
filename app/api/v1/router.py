from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.shared.config import APISettings

settings = APISettings()

# Роутер, отвечающий за подключение сервисных роутеров
router = APIRouter(prefix=settings.v1_prefix)
router.include_router(health_router)
