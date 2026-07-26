from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Настройки приложения"""
    name: str
    version: str
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="APP_", case_sensitive=False)


class DatabaseSettings(BaseSettings):
    """Настройки базы данных"""
    _engine: str
    _driver: str
    host: str
    port: int
    name: str
    user: str
    password: str

    @property
    def url(self) -> str:
        return f"{self._engine}+{self._driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_prefix="DB_", case_sensitive=False)


class ServerSettings(BaseSettings):
    """Настройки сервера"""
    host: str = "127.0.0.1"
    port: int = 8000

    model_config = SettingsConfigDict(env_prefix="SERVER_", case_sensitive=False)


class JWTSettings(BaseSettings):
    """Настройки JWT-токена"""
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(env_prefix="JWT_", case_sensitive=False)


class Settings(BaseSettings):
    """Настройки приложения"""
    app: AppSettings = Field(default_factory=AppSettings)
    db: DatabaseSettings = Field(default_factory=DatabaseSettings)
    server: ServerSettings = Field(default_factory=ServerSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
