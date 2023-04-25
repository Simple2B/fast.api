from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.fixture import TestData


def test_admin_auth(client: TestClient, db: Session, test_data: TestData):
    # login by email and password
    su_data = {
        "email": test_data.test_superuser.email,
        "password": test_data.test_superuser.password,
    }
    response = client.post("admin/login", data=su_data)
    assert response and response.status_code == 200
