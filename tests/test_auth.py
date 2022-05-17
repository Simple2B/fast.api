import pytest
import asyncio
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.main import app
from app.models import User
from app.database import Base, get_db


@pytest.fixture()
def client() -> Generator:

    with TestClient(app) as c:
        yield c


@pytest.fixture()
def db() -> Generator:
    # SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:

        def override_get_db() -> Generator:
            yield db

        app.dependency_overrides[get_db] = override_get_db

        yield db
        Base.metadata.drop_all(bind=engine)


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
