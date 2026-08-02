from uuid import UUID

from uuid_extensions import uuid7

from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.value_objects import Email, FullName


class AccountFactory:
    @staticmethod
    def build(
        *,
        email: Email | None = None,
        full_name: FullName | None = None,
        is_active: bool | None = None,
        id: UUID | None = None,
    ) -> Account:
        return Account(
            id=(id if id is not None else uuid7()),
            email=(email if email is not None else Email("user@example.com")),
            full_name=(full_name if full_name is not None else FullName("Ivan Petrov")),
            is_active=(is_active if is_active is not None else True),
        )
