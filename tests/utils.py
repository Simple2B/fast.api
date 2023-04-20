from sqlalchemy.orm import Session

from tests.fixture import TestData

import app.model as m


def fill_db_by_test_data(db: Session, test_data: TestData):
    print("Filling up db with fake data")
    for u in test_data.test_users:
        db.add(m.User(**u.dict()))
        db.commit()
    for u in test_data.test_authorized_users:
        db.add(m.User(**u.dict()))
        db.commit()
