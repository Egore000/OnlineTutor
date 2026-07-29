from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI


# TODO: Настроить логгирование
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    yield
