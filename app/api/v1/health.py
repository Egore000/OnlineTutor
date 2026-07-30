from fastapi import APIRouter

from app.shared.config import Tag

router = APIRouter(
    prefix="/health",
    tags=[Tag.SYSTEM],
)


@router.get("/", summary="Проверка активности сервера")
async def health() -> dict[str, str]:
    return {"status": "ok"}
