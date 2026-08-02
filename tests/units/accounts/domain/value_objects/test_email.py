import pytest

from app.modules.accounts.domain.exceptions import InvalidEmailError
from app.modules.accounts.domain.value_objects import Email


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "user@example.com",
        "ivan.petrov@gmail.com",
        "12341@yandex.ru",
        "te$t31@irk.gov",
        "a@b.io",
    ],
)
def test_create_email(value: str) -> None:
    email = Email(value)
    assert email.value == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "test@@example.com",
        "user@",
        "user@example",
        "user@example..com",
        "user@.ru",
        "user@gmail.",
        "userexample.com",
        "@example.com",
        "user gmail.comtest user@gmail.comtest" * 14 + "1@mail.ru",
        "gmail.com",
    ],
)
def test_reject_invalid_email(value: str | None) -> None:
    with pytest.raises(InvalidEmailError):
        Email(value)  # type: ignore


@pytest.mark.unit
def test_email_is_normalized() -> None:
    email = Email("USER@MAIL.RU")

    assert email.value == "USER@mail.ru"


@pytest.mark.unit
def test_equal_emails() -> None:
    email1 = Email("user@example.com")
    email2 = Email("user@example.com")

    assert email1 == email2


@pytest.mark.unit
def test_not_equal_email() -> None:
    email1 = Email("user1@example.com")
    email2 = Email("user2@example.com")

    assert email1 != email2


@pytest.mark.unit
def test_email_str() -> None:
    email = Email("user@example.com")

    assert str(email) == "user@example.com"


@pytest.mark.unit
def test_email_is_hashable() -> None:
    emails = {Email("user@example.com"), Email("user@example.com")}
    assert len(emails) == 1
