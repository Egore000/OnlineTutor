from unittest.mock import AsyncMock, Mock

import pytest
from factories.account_factory import AccountFactory

from app.modules.accounts.application.commands import AuthAccountCommand
from app.modules.accounts.application.use_cases import AuthAccountUseCase
from app.modules.accounts.domain.exceptions import InvalidCredentialsError
from app.modules.accounts.domain.value_objects import Email


@pytest.mark.unit
async def test_auth_account() -> None:
    account = AccountFactory.build()

    hasher = Mock()
    hasher.verify.return_value = True

    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=account)

    use_case = AuthAccountUseCase(repository, hasher)
    command = AuthAccountCommand(
        email=Email("user@example.com"),
        password="hashed-password",
    )

    result = await use_case.execute(command)

    assert result is account
    repository.get_by_email.assert_awaited_once_with(command.email)
    hasher.verify.assert_called_once_with(command.password, account.password_hash)


@pytest.mark.unit
async def test_auth_account_not_found() -> None:
    hasher = Mock()
    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=None)

    use_case = AuthAccountUseCase(repository, hasher)

    command = AuthAccountCommand(
        email=Email("user@example.com"),
        password="password",
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(command)

    repository.get_by_email.assert_awaited_once_with(command.email)
    hasher.verify.assert_not_called()


@pytest.mark.unit
async def test_auth_account_incorrect_password() -> None:
    account = AccountFactory.build()

    hasher = Mock()
    hasher.verify.return_value = False

    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=account)

    use_case = AuthAccountUseCase(repository, hasher)

    command = AuthAccountCommand(
        email=Email("user@example.com"),
        password="password",
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(command)

    repository.get_by_email.assert_awaited_once_with(command.email)
    hasher.verify.assert_called_once_with(command.password, account.password_hash)


@pytest.mark.unit
async def test_auth_account_inactive() -> None:
    account = AccountFactory.build(is_active=False)

    hasher = Mock()

    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=account)

    use_case = AuthAccountUseCase(repository, hasher)

    command = AuthAccountCommand(
        email=Email("user@example.com"),
        password="password",
    )

    with pytest.raises(InvalidCredentialsError):
        await use_case.execute(command)

    repository.get_by_email.assert_awaited_once_with(command.email)
    hasher.verify.assert_not_called()
