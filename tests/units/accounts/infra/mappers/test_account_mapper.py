import pytest
from factories import AccountFactory
from uuid_extensions import uuid7

from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.value_objects import Email, FullName
from app.modules.accounts.infra.mappers import AccountMapper
from app.modules.accounts.infra.models import AccountModel


@pytest.mark.unit
def test_account_mapper_domain_to_model() -> None:
    account = AccountFactory.build()

    orm_account = AccountMapper.to_model(account)

    assert isinstance(orm_account, AccountModel)
    assert orm_account.id == account.id
    assert orm_account.email == account.email.value
    assert orm_account.full_name == account.full_name.value
    assert orm_account.is_active == account.is_active


@pytest.mark.unit
@pytest.mark.parametrize("is_active", [True, False])
def test_account_mapper_model_to_domain(is_active: bool) -> None:
    orm_account = AccountModel(
        id=uuid7(),
        email="user@example.com",
        full_name="Иванов Иван",
        is_active=is_active,
    )

    account = AccountMapper.to_domain(orm_account)

    assert isinstance(account, Account)

    assert account.id == orm_account.id

    assert isinstance(account.email, Email)
    assert account.email.value == orm_account.email

    assert isinstance(account.full_name, FullName)
    assert account.full_name.value == orm_account.full_name

    assert account.is_active is is_active


@pytest.mark.unit
def test_account_mapper_update_model() -> None:
    account_id = uuid7()

    orm_account = AccountModel(
        id=account_id, email="user@example.com", full_name="Иванов Иван", is_active=True
    )

    account = AccountFactory.build(
        id=account_id,
        email=Email("new_user@example.com"),
        full_name=FullName("Пётр Петров"),
        is_active=False,
    )

    AccountMapper.update_model(orm_account, account)

    assert orm_account.id == account.id
    assert orm_account.email == account.email.value
    assert orm_account.full_name == account.full_name.value
    assert orm_account.is_active == account.is_active
