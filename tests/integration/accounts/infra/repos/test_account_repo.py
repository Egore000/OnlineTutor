import pytest
from factories import AccountFactory
from sqlalchemy.ext.asyncio import AsyncSession

# from app.modules.accounts.domain.entities import Account
# from app.modules.accounts.infra.models import AccountModel
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
