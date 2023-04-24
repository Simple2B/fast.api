from sqlalchemy.orm import relationship

from app.database import Base
from .base_user import BaseUser


class User(Base, BaseUser):
    posts = relationship("Post", viewonly=True)

    __tablename__ = "users"
