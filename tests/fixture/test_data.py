from typing import Generator

import pytest
from pydantic import BaseModel


class TestUser(BaseModel):
    __test__ = False

    username: str
    email: str
    password: str
    is_verified: bool | None = True


class TestData(BaseModel):
    __test__ = False

    test_user: TestUser | None
    test_users: list[TestUser]

    # authorized
    test_authorized_users: list[TestUser]
    test_superuser: TestUser | None


@pytest.fixture
def test_data() -> Generator[TestData, None, None]:
    yield TestData.parse_file("tests/test_data.json")
