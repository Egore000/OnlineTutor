from typing import Protocol
from uuid import UUID


class TokenService(Protocol):
    """Сервис для работы с токенами"""

    def create_access_token(self, account_id: UUID) -> str: ...

    def decode_access_token(self, token: str) -> UUID: ...
