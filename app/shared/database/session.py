from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.shared.config import settings

engine: AsyncEngine = create_async_engine(settings.db.url, echo=settings.app.debug, future=True)


async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# TODO: Настроить логгирование
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
        finally:
            await session.close()
