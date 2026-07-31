from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.accounts.domain.exceptions import InvalidDatetimeError
from app.modules.accounts.domain.value_objects import Email, FullName


@dataclass(kw_only=True, slots=True)
class Account:
    """Аккаунт пользователя"""

    id: UUID
    email: Email
    full_name: FullName
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        if self.created_at > self.updated_at:
            raise InvalidDatetimeError
