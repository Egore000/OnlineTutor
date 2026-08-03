import pytest

from app.modules.accounts.infra.security.password_hasher import Argon2PasswordHasher


@pytest.mark.unit
async def test_hash_not_equal_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "password"
    hashed_password = hasher.hash(password)

    assert hashed_password != password


@pytest.mark.unit
async def test_verify_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "password"
    hashed_password = hasher.hash(password)

    assert hasher.verify(password, hashed_password)


@pytest.mark.unit
async def test_incorrect_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "password"
    hashed_password = hasher.hash(password)

    assert not hasher.verify("another-password", hashed_password)


@pytest.mark.unit
async def test_hashes_not_equal() -> None:
    hasher = Argon2PasswordHasher()

    password1 = "password"
    password2 = "password"
    hashed_password1 = hasher.hash(password1)
    hashed_password2 = hasher.hash(password2)

    assert hashed_password1 != hashed_password2

    assert hasher.verify(password1, hashed_password1)
    assert hasher.verify(password2, hashed_password2)
