from unittest.mock import AsyncMock, Mock

import pytest

from app.modules.accounts.application.commands import RegisterAccountCommand
from app.modules.accounts.application.use_cases import RegisterAccountUseCase
from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.exceptions import EmailAlreadyExistsError
from app.modules.accounts.domain.value_objects import Email, FullName


@pytest.mark.unit
async def test_register_account() -> None:
    hasher = Mock()
    hasher.hash.return_value = "hashed_password"

    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=None)
    repository.add = AsyncMock()

    use_case = RegisterAccountUseCase(
        repository=repository,
        hasher=hasher,
    )

    command = RegisterAccountCommand(
        email=Email("user@example.com"),
        full_name=FullName("Иванов Иван Иванович"),
        password="password",
    )

    await use_case.execute(command)

    repository.get_by_email.assert_called_once_with(command.email)
    repository.add.assert_awaited_once()

    hasher.hash.assert_called_once_with(command.password)

    account = repository.add.await_args.args[0]

    assert isinstance(account, Account)
    assert account.email == command.email
    assert account.full_name == command.full_name
    assert account.password_hash == "hashed_password"
    assert account.is_active is True


@pytest.mark.unit
async def test_register_account_raises_email_exists() -> None:
    hasher = Mock()
    hasher.hash.return_value = "hashed_password"

    repository = Mock()
    repository.get_by_email = AsyncMock(return_value=Mock())
    repository.add = AsyncMock()

    use_case = RegisterAccountUseCase(repository, hasher)

    command = RegisterAccountCommand(
        email=Email("user@example.com"),
        full_name=FullName("Иванов Иван"),
        password="password",
    )

    with pytest.raises(EmailAlreadyExistsError):
        await use_case.execute(command)

    repository.add.assert_not_awaited()
    hasher.hash.assert_not_called()
