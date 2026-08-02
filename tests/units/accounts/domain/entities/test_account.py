from uuid import UUID

import pytest
from factories import AccountFactory
from uuid_extensions import uuid7

from app.modules.accounts.domain.value_objects import Email, FullName


@pytest.mark.unit
def test_account_generate_id() -> None:
    account = AccountFactory.build()

    assert account.id is not None
    assert isinstance(account.id, UUID)


@pytest.mark.unit
def test_account_generates_unique_id() -> None:
    account1 = AccountFactory.build()
    account2 = AccountFactory.build()

    assert account1.id != account2.id


@pytest.mark.unit
def test_account_uses_provides_id() -> None:
    account_id = uuid7()

    account = AccountFactory.build(id=account_id)

    assert account.id == account_id


@pytest.mark.unit
def test_account_contains_value_objects() -> None:
    email = Email("user@example.com")
    full_name = FullName("Иванов Иван")

    account = AccountFactory.build(email=email, full_name=full_name)

    assert account.email is email
    assert account.full_name is full_name


@pytest.mark.unit
def test_account_activate() -> None:
    account = AccountFactory.build(is_active=False)

    account.activate()

    assert account.is_active


@pytest.mark.unit
def test_account_deactivate() -> None:
    account = AccountFactory.build()

    account.deactivate()

    assert not account.is_active


@pytest.mark.unit
def test_account_change_email() -> None:
    new_email = Email("new_email@example.com")

    account = AccountFactory.build()
    account.change_email(new_email)

    assert account.email is new_email


@pytest.mark.unit
def test_account_change_full_name() -> None:
    new_full_name = FullName("Петров Петр")

    account = AccountFactory.build()
    account.change_full_name(new_full_name)

    assert account.full_name is new_full_name
