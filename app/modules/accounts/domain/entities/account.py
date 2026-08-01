from dataclasses import dataclass
from uuid import UUID

from app.modules.accounts.domain.value_objects import Email, FullName


@dataclass(kw_only=True, slots=True)
class Account:
    """Аккаунт пользователя"""

    id: UUID
    email: Email
    full_name: FullName
    is_active: bool

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_email(self, new_email: Email) -> None:
        self.email = new_email

    def change_full_name(self, new_full_name: FullName) -> None:
        self.full_name = new_full_name
