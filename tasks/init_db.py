from sqlalchemy.orm import Session
from invoke import task
from app.config import settings
from app.model import User

NUM_TEST_USERS = 10
NUM_TEST_POSTS = 3


@task
def init_db(_, test_data=False):
    """Initialization database

    Args:
        --test-data (bool, optional): wether fill database by test data. Defaults to False.
    """
    from app.database import SessionLocal

    db = SessionLocal()
    # add admin user
    admin: User = User(
        username=settings.ADMIN_USER,
        password=settings.ADMIN_PASS,
        email=settings.ADMIN_EMAIL,
    )
    db.add(admin)
    if test_data:
        # Add test data
        fill_test_data(db)

    db.commit()


def fill_test_data(db: Session):
    from app.model import Post

    for uid in range(NUM_TEST_USERS):
        user = User(username=f"User{uid}", password="pa$$", email=f"user{uid}@test.com")
        db.add(user)
        db.commit()
        db.refresh(user)
        for pid in range(NUM_TEST_POSTS):
            db.add(
                Post(
                    title=f"Title{pid}",
                    content=(f"Test of post {pid}" * (pid + 1)),
                    user=user,
                )
            )
