import secrets

import pytest

from app.modules.accounts.infra.security.jwt_token_service import JWTTokenService


@pytest.fixture
def token_service() -> JWTTokenService:
    secret_key = secrets.token_urlsafe(64)
    return JWTTokenService(
        secret_key=secret_key,
        algorithm="HS256",
        expire_minutes=30,
    )
