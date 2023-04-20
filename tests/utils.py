from sqlalchemy.orm import Session


def fill_db_by_test_data(db: Session, test_data):
    print("Filling up db with fake data")
