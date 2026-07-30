from fastapi import APIRouter

from app.shared.config import Tag, settings

router = APIRouter(tags=[Tag.SYSTEM])


@router.get("/", summary="Получение информации o приложении")
async def get_app_info() -> dict[str, str]:
    return {
        "name": settings.app.name,
        "summary": settings.app.summary,
        "description": settings.app.description,
        "version": settings.app.version,
        "docs": "/docs",
    }
