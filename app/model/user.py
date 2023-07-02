from sqlalchemy.orm import relationship

from .base_user import BaseUser
from app.database import db


class User(db.Model, BaseUser):
    __tablename__ = "users"

    posts = relationship("Post", viewonly=True)
