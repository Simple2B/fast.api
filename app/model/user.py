# pyright: reportUndefinedVariable=none
import sqlalchemy.orm as orm

from .base_user import BaseUser
from app.database import db


class User(db.Model, BaseUser):
    __tablename__ = "users"

    posts: orm.Mapped[list["Post"]] = orm.relationship()
