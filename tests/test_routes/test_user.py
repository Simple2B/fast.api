from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.schema as s
from tests.fixture import TestData


def test_auth(client: TestClient, db: Session, test_data: TestData):
    request_data = s.BaseUser(
        username=test_data.test_users[0].username,
        email=test_data.test_users[0].email,
        password=test_data.test_users[0].password,
    )
    # login by username and password
    response = client.post("api/auth/login", data=request_data.dict())
    assert response and response.status_code == 200, "unexpected response"
