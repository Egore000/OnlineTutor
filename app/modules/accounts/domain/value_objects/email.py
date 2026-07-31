from dataclasses import dataclass

from app.modules.accounts.domain.exceptions import InvalidEmailError


@dataclass(slots=True, frozen=True)
class Email:
    """Адрес электронной почты"""

    value: str

    def __post_init__(self) -> None:
        # Проверка вхождения только одного символа "@"
        if ("@" not in self.value) or (self.value.count("@") != 1):
            raise InvalidEmailError

        local, domain = self.value.split("@")

        # Проверка наличия и размера названия почты
        if (not local) or (len(local) > 64):
            raise InvalidEmailError

        # Проверка наличия почтового домена и содержания в нём только одного символа "."
        if (not domain) or ("." not in domain) or (domain.count(".") != 1):
            raise InvalidEmailError

    def __str__(self) -> str:
        return self.value
