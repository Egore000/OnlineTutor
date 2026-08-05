from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class GetAccountCommand:
    """Запрос на получение информации об аккаунте"""

    account_id: UUID
