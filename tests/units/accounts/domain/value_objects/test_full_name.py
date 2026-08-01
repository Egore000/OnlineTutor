import pytest

from app.modules.accounts.domain.exceptions import InvalidFullNameError
from app.modules.accounts.domain.value_objects import FullName


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        "Иванов Иван Иванович",
        "Вася Васин",
        "John Jackson",
        "Jake Mc'Donalds",
        "Виктор Иванов-Петров",
    ],
)
def test_create_full_name(value: str | None) -> None:
    full_name = FullName(value)  # type: ignore

    assert full_name.value == value


@pytest.mark.unit
@pytest.mark.parametrize(
    "value",
    [
        None,
        "",
        "Иван1 Иванов2",
        "Иван" * 40 + "a",
        "123",
    ],
)
def test_reject_invalid_full_name(value: str | None) -> None:
    with pytest.raises(InvalidFullNameError):
        FullName(value)  # type: ignore


@pytest.mark.unit
def test_full_name_is_normalized() -> None:
    full_name = FullName("  Иванов   Иван  ")

    assert full_name.value == "Иванов Иван"


@pytest.mark.unit
def test_equal_full_name() -> None:
    full_name1 = FullName("Иванов Иван")
    full_name2 = FullName("Иванов Иван")

    assert full_name1 == full_name2


@pytest.mark.unit
def test_not_equal_full_name() -> None:
    full_name1 = FullName("Иванов Иван")
    full_name2 = FullName("Петров Перт")

    assert full_name1 != full_name2


@pytest.mark.unit
def test_full_name_str() -> None:
    full_name = FullName("Иванов Иван")

    assert str(full_name) == "Иванов Иван"


@pytest.mark.unit
def test_full_name_is_hashable() -> None:
    names = {
        FullName("Иванов Иван"),
        FullName("Иванов Иван"),
    }
    assert len(names) == 1
