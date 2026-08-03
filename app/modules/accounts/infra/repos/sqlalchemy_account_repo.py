from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.exceptions import AccountNotFoundError
from app.modules.accounts.domain.repos import AccountRepository
from app.modules.accounts.domain.value_objects import Email
from app.modules.accounts.infra.mappers import AccountMapper
from app.modules.accounts.infra.models import AccountModel


class SQLAlchemyAccountRepository(AccountRepository):
    """Реализация репозитория AccountRepository через SQLAlchemy"""

    _mapper: type[AccountMapper] = AccountMapper

    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, account: Account) -> None:
        """Создание нового аккаунта"""

        account_model = self._mapper.to_model(account)
        self._session.add(account_model)

    async def get_by_id(self, account_id: UUID) -> Account | None:
        """Поиск аккаунта по ID"""

        model = await self._session.get(AccountModel, account_id)
        if model is None:
            return None

        return self._mapper.to_domain(model)

    async def get_by_email(self, email: Email) -> Account | None:
        """Поиск аккаунта по электронной почте"""

        stmt = select(AccountModel).where(AccountModel.email == email.value)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return self._mapper.to_domain(model)

    async def update(self, account: Account) -> None:
        """Обновление данных в аккаунте"""

        model = await self._session.get(AccountModel, account.id)

        if model is None:
            raise AccountNotFoundError(account.id)

        self._mapper.update_model(model, account)

    async def delete(self, account_id: UUID) -> None:
        """Удаление аккаунта"""

        model = await self._session.get(AccountModel, account_id)

        if model is None:
            raise AccountNotFoundError(account_id)

        await self._session.delete(model)

    async def commit(self) -> None:
        await self._session.commit()
