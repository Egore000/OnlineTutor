from dataclasses import dataclass

from app.modules.accounts.domain.exceptions import InvalidFullNameError


@dataclass(frozen=True, slots=True)
class FullName:
    """Полное имя"""

    value: str

    def __post_init__(self) -> None:
        # Проверка типа
        if not isinstance(self.value, str):
            raise InvalidFullNameError

        # Проверка наличия цифр
        if any(ch.isdigit() for ch in self.value):
            raise InvalidFullNameError

        # Проверка длины имени
        if not (0 < len(self.value) <= 80):
            raise InvalidFullNameError

        # Нормализация
        normalized = " ".join(self.value.strip().split())

        # Проверка на пустоту после нормализации
        if not normalized:
            raise InvalidFullNameError

        object.__setattr__(self, "value", normalized)

    def __str__(self) -> str:
        return self.value
