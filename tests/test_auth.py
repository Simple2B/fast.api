from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import User


def test_auth(client: TestClient, db: Session):
    USER_NAME = "michael"
    USER_EMAIL = "test@test.ku"
    USER_PASSWORD = "secret"
    data = {"username": USER_NAME, "email": USER_EMAIL, "password": USER_PASSWORD}
    response = client.post("/user/", json=data)
    assert response
    assert response.ok
    user = db.query(User).filter(User.username == data["username"]).first()
    assert user
    assert user.username == data["username"]

    response = client.post(
        "/login", data=dict(username=USER_NAME, password=USER_PASSWORD)
    )
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert "access_token" in data
    token = data["access_token"]
    assert token
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get(f"/user/{1}", headers=headers)
    assert response
    assert response.ok
    data = response.json()
    assert data
    assert "username" in data
    assert data["username"] == USER_NAME
