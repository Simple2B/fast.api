from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s


def test_auth(client: TestClient, db: Session):
    USER_NAME = "michael"
    USER_EMAIL = "test@test.ku"
    USER_PASSWORD = "secret"
    # data = {"username": USER_NAME, "email": USER_EMAIL, "password": USER_PASSWORD}
    data = s.BaseUser(
        username=USER_NAME,
        email=USER_EMAIL,
        password=USER_PASSWORD,
    )
    # create new user
    response = client.post("/user/", json=data.dict())
    assert response

    new_user = s.User.parse_obj(response.json())
    user = db.query(m.User).get(new_user.id)
    assert user.username == new_user.username

    # login by username and password
    response = client.post(
        "/login", data=dict(username=USER_NAME, password=USER_PASSWORD)
    )
    assert response and response.ok, "unexpected response"
    token = s.Token.parse_obj(response.json())
    headers = {"Authorization": f"Bearer {token.access_token}"}

    # get user by id
    response = client.get(f"/user/{new_user.id}", headers=headers)
    assert response and response.ok
    user = s.UserOut.parse_obj(response.json())
    assert user.username == USER_NAME
