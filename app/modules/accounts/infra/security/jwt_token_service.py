from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.modules.accounts.application.services.token_service import TokenService
from app.modules.accounts.domain.exceptions import InvalidTokenError
from app.shared.config import JWTSettings

jwt_settings = JWTSettings()


class JWTTokenServcie(TokenService):
    """Реализация сервиса работы с токенами на базе JWT"""

    def __init__(self, secret_key: str, algorithm: str) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm

    def create_access_token(self, account_id: UUID) -> str:
        now = datetime.now(UTC)
        exp = now + timedelta(minutes=jwt_settings.access_token_expire_minutes)

        payload = {
            "sub": str(account_id),
            "exp": exp,
            "iat": now,
        }
        try:
            return jwt.encode(payload, self._secret_key, self._algorithm)
        except jwt.exceptions.PyJWTError as exc:
            raise InvalidTokenError from exc

    def decode_access_token(self, token: str) -> UUID:
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
        except jwt.exceptions.InvalidTokenError as exc:
            raise InvalidTokenError from exc

        subject = payload.get("sub")

        if subject is None:
            raise InvalidTokenError

        try:
            return UUID(subject)
        except ValueError as exc:
            raise InvalidTokenError from exc
