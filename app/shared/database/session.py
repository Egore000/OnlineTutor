from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.shared.config import AppSettings, get_db_url, settings

DATABASE_URL = get_db_url(settings)
app_settings = AppSettings()


engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=app_settings.debug, future=True)


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
