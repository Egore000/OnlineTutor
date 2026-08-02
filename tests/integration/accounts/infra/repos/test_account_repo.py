import pytest
from factories import AccountFactory
from sqlalchemy.ext.asyncio import AsyncSession
from uuid_extensions import uuid7

from app.modules.accounts.domain.exceptions import AccountNotFoundError
from app.modules.accounts.domain.value_objects import Email, FullName
from app.modules.accounts.infra.repos import SQLAlchemyAccountRepository


@pytest.mark.integration
async def test_add_account(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    account = AccountFactory.build()

    await repository.add(account)
    await session.flush()

    result = await repository.get_by_id(account.id)

    assert result is not None
    assert result.id == account.id
    assert result.email == account.email
    assert result.full_name == account.full_name
    assert result.is_active == account.is_active


@pytest.mark.integration
async def test_get_account_by_id(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    account = AccountFactory.build()

    await repository.add(account)
    await session.flush()

    result = await repository.get_by_id(account.id)

    assert result is not None
    assert result.id == account.id
    assert result.email == account.email
    assert result.full_name == account.full_name
    assert result.is_active == account.is_active


@pytest.mark.integration
async def test_get_account_by_id_returns_none(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    result = await repository.get_by_id(uuid7())

    assert result is None


@pytest.mark.integration
async def test_get_account_by_email(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    account = AccountFactory.build()

    await repository.add(account)
    await session.flush()

    result = await repository.get_by_email(account.email)

    assert result is not None
    assert result.id == account.id
    assert result.email == account.email
    assert result.full_name == account.full_name
    assert result.is_active == account.is_active


@pytest.mark.integration
async def test_get_account_by_email_returns_none(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    result = await repository.get_by_email(Email("test@example.com"))

    assert result is None


@pytest.mark.integration
async def test_update_account(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    account = AccountFactory.build()

    await repository.add(account)
    await session.flush()

    updated_account = AccountFactory.build(
        id=account.id,
        email=Email("new_email@example.com"),
        full_name=FullName("Семёнов Семён"),
        is_active=False,
    )

    await repository.update(updated_account)
    await session.flush()

    result = await repository.get_by_id(account.id)

    assert result is not None
    assert result.id == updated_account.id == account.id
    assert result.email == updated_account.email
    assert result.full_name == updated_account.full_name
    assert result.is_active == updated_account.is_active


@pytest.mark.integration
async def test_update_account_raises_if_account_not_found(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)

    updated_account = AccountFactory.build()

    with pytest.raises(AccountNotFoundError):
        await repository.update(updated_account)


@pytest.mark.integration
async def test_delete_account(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)
    account = AccountFactory.build()
    await repository.add(account)
    await session.flush()

    await repository.delete(account.id)
    await session.flush()

    result = await repository.get_by_id(account.id)
    assert result is None


@pytest.mark.integration
async def test_delete_account_raises_if_account_not_found(session: AsyncSession) -> None:
    repository = SQLAlchemyAccountRepository(session=session)
    account = AccountFactory.build()

    with pytest.raises(AccountNotFoundError):
        await repository.delete(account.id)
