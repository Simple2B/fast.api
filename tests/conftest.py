from functools import lru_cache

from dotenv import dotenv_values
from app.config import Settings
from app import config


@lru_cache
def get_test_settings() -> Settings:
    return Settings(**dotenv_values("tests/test.env"))


pytest_plugins = [
    "tests.fixture.db",
    "tests.fixture.client",
    "tests.fixture.mail_client",
    "tests.fixture.test_data",
]

config.get_settings = get_test_settings
