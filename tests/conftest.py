import logging
import os
from collections.abc import AsyncGenerator

import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

os.environ["MODE"] = "TEST"

from app.modules.accounts.infra.models import AccountModel  # noqa: F401
from app.shared.config import settings
from app.shared.database.base import Base

logger = logging.getLogger("tests")

logger.info("[TEST] APP_MODE=%s", settings.mode)
logger.info("[TEST] DATABASE=%s", settings.database_url)

engine = create_async_engine(
    settings.database_url,
    echo=False,
    poolclass=NullPool,
)

session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture
async def prepare_database() -> AsyncGenerator[None, None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()
