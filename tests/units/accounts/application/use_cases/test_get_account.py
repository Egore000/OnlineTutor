from unittest.mock import AsyncMock, Mock

import pytest
from factories.account_factory import AccountFactory
from uuid_extensions import uuid7

from app.modules.accounts.application.commands.get_account import GetAccountCommand
from app.modules.accounts.application.use_cases import GetAccountUseCase
from app.modules.accounts.domain.exceptions import AccountNotFoundError


@pytest.mark.unit
async def test_get_account_success() -> None:
    account = AccountFactory.build()

    repository = Mock()
    repository.get_by_id = AsyncMock(return_value=account)

    use_case = GetAccountUseCase(repository)
    command = GetAccountCommand(account.id)

    result = await use_case.execute(command)

    assert result is not None
    assert result == account


@pytest.mark.unit
async def test_get_account_failed_not_found() -> None:
    repository = Mock()
    repository.get_by_id = AsyncMock(return_value=None)

    use_case = GetAccountUseCase(repository)
    command = GetAccountCommand(uuid7())

    with pytest.raises(AccountNotFoundError):
        await use_case.execute(command)
