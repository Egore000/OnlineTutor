from dataclasses import dataclass

from app.modules.accounts.domain.exceptions import InvalidFullNameError


@dataclass(frozen=True, slots=True)
class FullName:
    """Полное имя"""

    value: str

    def __post_init__(self) -> None:
        if not (0 < len(self.value) <= 80):
            raise InvalidFullNameError

        normalized = " ".join(self.value.strip().split())

        if not normalized:
            raise InvalidFullNameError

        object.__setattr__(self, "value", normalized)
