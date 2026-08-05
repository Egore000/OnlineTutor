from datetime import UTC, datetime, timedelta
from uuid import UUID

import jwt

from app.modules.accounts.application.services.token_service import TokenService
from app.modules.accounts.domain.exceptions import InvalidTokenError


class JWTTokenService(TokenService):
    """Реализация сервиса работы с токенами на базе JWT"""

    def __init__(
        self,
        secret_key: str,
        algorithm: str,
        expire_minutes: int = 30,
    ) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_access_token(self, account_id: UUID) -> str:
        now = datetime.now(UTC)
        exp = now + timedelta(minutes=self._expire_minutes)

        payload = {
            "sub": str(account_id),
            "exp": exp,
            "iat": now,
        }
        return jwt.encode(payload, self._secret_key, self._algorithm)

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
