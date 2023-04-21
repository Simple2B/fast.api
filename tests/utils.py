from sqlalchemy.orm import Session

from tests.fixture import TestData

import app.model as m


def fill_db_by_test_data(db: Session, test_data: TestData):
    print("Filling up db with fake data")
    for u in test_data.test_users:
        db.add(
            m.User(
                username=u.username,
                email=u.email,
                password=u.password,
                is_verified=u.is_verified,
            )
        )
        db.commit()
    for u in test_data.test_authorized_users:
        db.add(
            m.User(
                username=u.username,
                email=u.email,
                password=u.password,
                is_verified=u.is_verified,
            )
        )
        db.commit()
