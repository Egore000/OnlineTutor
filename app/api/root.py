from fastapi import APIRouter

from app.shared.config import AppSettings, Tag

settings = AppSettings()

router = APIRouter(tags=[Tag.SYSTEM])


@router.get("/", summary="Получение информации o приложении")
async def get_app_info() -> dict[str, str]:
    return {
        "name": settings.name,
        "summary": settings.summary,
        "description": settings.description,
        "version": settings.version,
        "docs": "/docs",
    }
