import pytest
from typing import Generator
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Generator:
    from app.main import app

    with TestClient(app) as c:
        yield c


# @pytest.fixture
# def authorized_coach_tokens(
#     client: TestClient,
#     db: Session,
#     test_data: TestData,
# ) -> Generator[list[s.Token], None, None]:
#     tokens = []
#     for user in test_data.test_authorized_coaches:
#         response = client.post(
#             "api/auth/coach/login/",
#             data={
#                 "username": user.email,
#                 "password": user.password,
#             },
#         )

#         assert response
#         token = s.Token.parse_obj(response.json())
#         tokens += [token]
#     yield tokens
