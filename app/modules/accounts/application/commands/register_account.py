from dataclasses import dataclass

from app.modules.accounts.domain.value_objects import Email, FullName


@dataclass(frozen=True, kw_only=True, slots=True)
class RegisterAccountCommand:
    """Данные для регистрации аккаунта"""

    email: Email
    full_name: FullName
    password: str
