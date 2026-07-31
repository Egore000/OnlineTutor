from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database.base import Base


class Account(Base):
    """SQLAlchemy ORM-модель аккаунта пользователя"""

    email: Mapped[str] = mapped_column(String(256), unique=True, primary_key=True)
    full_name: Mapped[str] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(default=True)
