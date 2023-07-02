from app.database import db
from .base_user import BaseUser


class SuperUser(db.Model, BaseUser):
    __tablename__ = "superusers"
