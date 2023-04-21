from datetime import datetime
from typing import Self

from sqlalchemy import Column, Integer, String, DateTime, Boolean, func, or_
from sqlalchemy.orm import relationship

from app.hash_utils import make_hash, hash_verify
from app.database import Base, SessionLocal
from app.utils import generate_uuid


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    uuid = Column(String(36), default=generate_uuid)

    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(128), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    is_verified = Column(Boolean, default=False)

    posts = relationship("Post", viewonly=True)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db: SessionLocal, email: str, password: str) -> Self:
        user = (
            db.query(cls)
            .filter(
                or_(
                    func.lower(cls.username) == func.lower(email),
                    func.lower(cls.email) == func.lower(email),
                )
            )
            .first()
        )
        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.username}>"
