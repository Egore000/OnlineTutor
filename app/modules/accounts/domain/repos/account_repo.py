from typing import Protocol
from uuid import UUID

from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.value_objects import Email


class AccountRepository(Protocol):
    """Репозиторий для работы c сущностью Account"""

    async def add(self, account: Account) -> None: ...

    async def get_by_id(self, account_id: UUID) -> Account | None: ...

    async def get_by_email(self, email: Email) -> Account | None: ...

    async def update(self, account: Account) -> None: ...

    async def delete(self, account_id: UUID) -> None: ...
