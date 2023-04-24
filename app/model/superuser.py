from app.database import Base
from .base_user import BaseUser


class SuperUser(Base, BaseUser):
    __tablename__ = "superusers"
