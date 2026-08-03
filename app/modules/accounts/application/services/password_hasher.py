from typing import Protocol


class PasswordHasher(Protocol):
    """Сервисный класс для хэширования пароля"""

    def hash(self, password: str) -> str: ...

    def verify(self, password: str, password_hash: str) -> bool: ...
