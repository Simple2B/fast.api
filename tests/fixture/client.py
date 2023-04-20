from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.schema as s
from .test_data import TestData


@pytest.fixture
def client() -> Generator:
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def authorized_users_tokens(
    client: TestClient,
    db: Session,
    test_data: TestData,
) -> Generator[list[s.Token], None, None]:
    tokens = []
    for user in test_data.test_authorized_users:
        response = client.post(
            "api/auth/login",
            data={
                "username": user.email,
                "password": user.password,
            },
        )

        assert response and response.status_code == 200
        token = s.Token.parse_obj(response.json())
        tokens += [token]
    yield tokens
