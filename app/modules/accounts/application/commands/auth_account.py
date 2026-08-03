from dataclasses import dataclass

from app.modules.accounts.domain.value_objects import Email


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthAccountCommand:
    """Данные для входа в систему"""

    email: Email
    password: str
