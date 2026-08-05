import os

os.environ["MODE"] = "TEST"


pytest_plugins = [
    "tests.fixtures.accounts",
    "tests.fixtures.database",
    "tests.fixtures.security",
]
