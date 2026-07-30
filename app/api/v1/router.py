from fastapi import APIRouter

from app.shared.config import settings

router = APIRouter(prefix=settings.api.v1_prefix)


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
