from typing import Generator

import pytest
from sqlalchemy.orm import sessionmaker
from tests.conftest import get_test_settings
from sqlalchemy.engine import create_engine

from app.config import Settings
from app.database import Base, get_db
from .test_data import TestData
from tests.utils import fill_db_by_test_data


@pytest.fixture
def db(test_data: TestData) -> Generator:
    from app.main import app

    settings: Settings = get_test_settings()

    engine = create_engine(settings.DB_URI, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestingSessionLocal() as db:
        fill_db_by_test_data(db, test_data)

        def override_get_db() -> Generator:
            try:
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db

        yield db
