from datetime import datetime
from typing import Self
import sqlalchemy as sa
import sqlalchemy.orm as orm


from app.hash_utils import make_hash, hash_verify
from app.utils import generate_uuid


class BaseUser:
    id = sa.Column(sa.Integer, primary_key=True)

    uuid = sa.Column(sa.String(36), default=generate_uuid)

    email = sa.Column(sa.String(128), nullable=False, unique=True)
    username = sa.Column(sa.String(64), nullable=False, unique=True)
    password_hash = sa.Column(sa.String(128), nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    is_verified = sa.Column(sa.Boolean, default=False)

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, value: str):
        self.password_hash = make_hash(value)

    @classmethod
    def authenticate(cls, db: orm.Session, user_id: str, password: str) -> Self | None:
        query = sa.select(cls).where(
            sa.or_(cls.username == user_id, cls.email == user_id)
        )
        user = db.execute(query).scalar_one_or_none()

        if user is not None and hash_verify(password, user.password):
            return user

    def __repr__(self):
        return f"<{self.id}: {self.email}>"
