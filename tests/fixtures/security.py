import secrets
from dataclasses import dataclass

import pytest

from app.modules.accounts.infra.security.jwt_token_service import JWTTokenService


@dataclass(frozen=True)
class JWTTestSettings:
    secret_key: str = secrets.token_urlsafe(64)
    algorithm: str = "HS256"
    expire_minutes: int = 30


@pytest.fixture
def jwt_settings() -> JWTTestSettings:
    return JWTTestSettings()


@pytest.fixture
def token_service(jwt_settings: JWTTestSettings) -> JWTTokenService:
    return JWTTokenService(
        secret_key=jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
        expire_minutes=jwt_settings.expire_minutes,
    )
