from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


AppMode = Literal["DEV", "TEST", "PROD"]


class AppSettings(BaseSettings):
    """Настройки приложения"""

    name: str
    version: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""

    engine: str
    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"{self.engine}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class TestSettings(BaseSettings):
    """Тестовые настройки"""

    database_url: str

    model_config = SettingsConfigDict(
        env_prefix="TEST_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class ServerSettings(BaseSettings):
    """Настройки сервера"""

    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_prefix="SERVER_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class JWTSettings(BaseSettings):
    """Настройки JWT-токена"""

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class Settings(BaseSettings):
    """Настройки приложения"""

    mode: AppMode = "DEV"

    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    test: TestSettings = Field(default_factory=TestSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)

    @property
    def database_url(self) -> str:
        if self.mode == "TEST":
            return self.test.database_url
        return self.db.url

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
