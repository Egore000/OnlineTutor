from app.modules.accounts.domain.entities import Account
from app.modules.accounts.domain.value_objects import Email, FullName
from app.modules.accounts.infra.models import AccountModel


class AccountMapper:
    """Статический класс для отображения доменной модели в ORM"""

    @staticmethod
    def to_domain(account: AccountModel) -> Account:
        """ORM -> Domain"""

        return Account(
            id=account.id,
            email=Email(account.email),
            full_name=FullName(account.full_name),
            is_active=account.is_active,
        )

    @staticmethod
    def to_model(account: Account) -> AccountModel:
        """Domain -> ORM"""

        return AccountModel(
            id=account.id,
            email=account.email.value,
            full_name=account.full_name.value,
            is_active=account.is_active,
        )

    @staticmethod
    def update_model(model: AccountModel, entity: Account) -> None:
        """Обновление ORM-модели полями из доменной модели"""

        model.email = entity.email.value
        model.full_name = entity.full_name.value
        model.is_active = entity.is_active
