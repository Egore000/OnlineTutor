from app.modules.accounts.application.commands import RegisterAccountCommand
from app.modules.accounts.application.services import PasswordHasher
from app.modules.accounts.domain.entities.account import Account
from app.modules.accounts.domain.exceptions import EmailAlreadyExistsError
from app.modules.accounts.domain.repos import AccountRepository


class RegisterAccountUseCase:
    """UseCase регистрации аккаунта"""

    def __init__(self, repository: AccountRepository, hasher: PasswordHasher) -> None:
        self._repository = repository
        self._hasher = hasher

    async def execute(self, command: RegisterAccountCommand) -> Account:
        existing_account = await self._repository.get_by_email(command.email)

        if existing_account is not None:
            raise EmailAlreadyExistsError

        password_hash = self._hasher.hash(command.password)
        account = Account(
            email=command.email,
            full_name=command.full_name,
            password_hash=password_hash,
            is_active=True,
        )
        await self._repository.add(account)
        return account
