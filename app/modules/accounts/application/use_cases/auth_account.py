from app.modules.accounts.application.commands.auth_account import AuthAccountCommand
from app.modules.accounts.application.services import PasswordHasher
from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.exceptions import InvalidCredentialsError
from app.modules.accounts.domain.repos import AccountRepository


class AuthAccountUseCase:
    """Use case для аутентификации аккаунта"""

    def __init__(
        self,
        repository: AccountRepository,
        hasher: PasswordHasher,
    ) -> None:
        self._repository = repository
        self._hasher = hasher

    async def execute(self, command: AuthAccountCommand) -> Account:
        existing = await self._repository.get_by_email(command.email)
        if existing is None:
            raise InvalidCredentialsError

        if not existing.is_active:
            raise InvalidCredentialsError

        password_correct = self._hasher.verify(command.password, existing.password_hash)

        if not password_correct:
            raise InvalidCredentialsError

        return existing
