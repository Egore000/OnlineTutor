import secrets
from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt
import pytest
from fixtures.security import JWTTestSettings
from uuid_extensions import uuid7

from app.modules.accounts.domain.exceptions import InvalidTokenError
from app.modules.accounts.infra.security.jwt_token_service import JWTTokenService


@pytest.mark.unit
def test_create_access_token(token_service: JWTTokenService, jwt_settings: JWTTestSettings) -> None:
    account_id = uuid7()

    token = token_service.create_access_token(account_id)
    assert isinstance(token, str)
    assert token.count(".") == 2

    payload = jwt.decode(token, key=jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
    assert payload["sub"] == str(account_id)
    assert "exp" in payload
    assert "iat" in payload


@pytest.mark.unit
def test_decode_access_token(token_service: JWTTokenService) -> None:
    account_id = uuid7()

    token = token_service.create_access_token(account_id)
    decoded_account_id = token_service.decode_access_token(token)

    assert isinstance(decoded_account_id, UUID)
    assert account_id == decoded_account_id


@pytest.mark.unit
def test_invalid_signature(token_service: JWTTokenService, jwt_settings: JWTTestSettings) -> None:
    account_id = uuid7()

    invalid_secret_key = secrets.token_urlsafe(32)
    invalid_token = jwt.encode(
        {"sub": str(account_id)},
        key=invalid_secret_key,
        algorithm=jwt_settings.algorithm,
    )

    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(invalid_token)


@pytest.mark.unit
def test_expired_token(token_service: JWTTokenService, jwt_settings: JWTTestSettings) -> None:
    expired_token = jwt.encode(
        {
            "sub": str(uuid7()),
            "exp": datetime.now(UTC) - timedelta(minutes=1),
        },
        key=jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(expired_token)


@pytest.mark.unit
def test_invalid_sub(token_service: JWTTokenService, jwt_settings: JWTTestSettings) -> None:
    token = jwt.encode(
        {"sub": "not-uuid-account_id"},
        key=jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(token)


@pytest.mark.unit
def test_missing_sub(token_service: JWTTokenService, jwt_settings: JWTTestSettings) -> None:
    token = jwt.encode(
        {},
        key=jwt_settings.secret_key,
        algorithm=jwt_settings.algorithm,
    )
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token(token)


@pytest.mark.unit
def test_invalid_token(token_service: JWTTokenService) -> None:
    with pytest.raises(InvalidTokenError):
        token_service.decode_access_token("some-token")
