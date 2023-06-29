from invoke import task

from app.logger import log
from app.database import get_db
from app.model import SuperUser
from app.config import get_settings


cfg = get_settings()

db = get_db().__next__()

SU_EMAIL = cfg.ADMIN_EMAIL
SU_PASSWORD = cfg.ADMIN_PASS


@task
def create_superuser(_, email: str = SU_EMAIL, password: str = SU_PASSWORD):
    """Create a superuser"""
    su = db.query(SuperUser).filter_by(email=email).first()
    if not su:
        su = SuperUser(email=email, username=email, password=password)
        db.add(su)
        db.commit()
        log(log.INFO, "SuperUser %s created", email)
    else:
        log(log.WARNING, "SuperUser -%s already exists", email)
