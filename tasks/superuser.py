from invoke import task

from app.logger import log
from app.database import get_db
from app.model import SuperUser

db = get_db().__next__()


SU_EMAIL = "admin@gmail.com"
SU_PASSWORD = "password"


@task
def create_superuser(_):
    su = db.query(SuperUser).filter_by(email=SU_EMAIL).first()
    if not su:
        su = SuperUser(email=SU_EMAIL, username=SU_EMAIL, password=SU_PASSWORD)
        db.add(su)
        db.commit()
        log(log.INFO, "SuperUser %s created", SU_EMAIL)
    else:
        log(log.WARNING, "SuperUser -%s already exists", SU_EMAIL)
