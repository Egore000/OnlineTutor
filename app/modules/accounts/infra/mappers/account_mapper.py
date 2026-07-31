from app.modules.accounts.domain.entities.account import Account
from app.modules.accounts.domain.value_objects import Email, FullName
from app.modules.accounts.infra.models.account_model import AccountModel


class AccountMapper:
    """Класс для отображения доменной модели в ORM"""

    @staticmethod
    def to_domain(account: AccountModel) -> Account:
        """ORM -> Domain"""

        return Account(
            id=account.id,
            email=Email(account.email),
            full_name=FullName(account.full_name),
            is_active=account.is_active,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )

    @staticmethod
    def to_model(account: Account) -> AccountModel:
        """Domain -> ORM"""

        return AccountModel(
            id=account.id,
            email=account.email.value,
            full_name=account.full_name.value,
            is_actie=account.is_active,
            created_at=account.created_at,
            updated_at=account.updated_at,
        )
