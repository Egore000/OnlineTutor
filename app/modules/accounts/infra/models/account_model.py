from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class AccountModel(Base):
    """SQLAlchemy ORM-модель аккаунта пользователя"""

    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(default=True)
