from app.modules.accounts.application.commands import GetAccountCommand
from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.exceptions import AccountNotFoundError
from app.modules.accounts.domain.repos import AccountRepository


class GetAccountUseCase:
    """Use case для получения информации об аккаунте"""

    def __init__(self, repository: AccountRepository) -> None:
        self._repository = repository

    async def execute(self, command: GetAccountCommand) -> Account:
        account = await self._repository.get_by_id(command.account_id)

        if account is None:
            raise AccountNotFoundError

        return account
