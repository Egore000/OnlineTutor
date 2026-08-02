from enum import StrEnum
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


AppMode = Literal["DEV", "TEST", "PROD"]


class Tag(StrEnum):
    SYSTEM = "Система"
    ACCOUNTS = "Аккаунты"
    STUDENTS = "Ученики"
    LESSONS = "Занятия"
    HOMEWORKS = "Домашние задания"


class AppSettings(BaseSettings):
    """Настройки приложения"""

    name: str
    summary: str
    description: str
    version: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class APISettings(BaseSettings):
    """Конфигурация API"""

    prefix: str = "/api"
    v1_prefix: str = "/v1"

    model_config = SettingsConfigDict(
        env_prefix="API_",
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
        env_file=BASE_DIR / ".env",
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


class LoggingSettings(BaseSettings):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    model_config = SettingsConfigDict(
        env_prefix="LOG_",
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


class Settings(BaseSettings):
    """Настройки приложения"""

    mode: AppMode = "DEV"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()


def get_db_url(settings: Settings) -> str:
    if settings.mode == "TEST":
        return TestSettings().database_url
    return DatabaseSettings().url
