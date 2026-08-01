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
