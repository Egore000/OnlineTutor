from fastapi import APIRouter

router = APIRouter(prefix="/health")


@router.get("/")
async def health() -> dict[str, str]:
    raise ValueError
    return {"status": "ok"}
