from datetime import datetime
from typing import Self
import sqlalchemy as sa
import sqlalchemy.orm as orm


from app.hash_utils import make_hash, hash_verify
from app.utils import generate_uuid


class BaseUser:
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid)

    email: orm.Mapped[str] = orm.mapped_column(
        sa.String(128), nullable=False, unique=True
    )
    username: orm.Mapped[str] = orm.mapped_column(
        sa.String(64), nullable=False, unique=True
    )
    password_hash: orm.Mapped[str] = orm.mapped_column(sa.String(128), nullable=False)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.now
    )
    is_verified: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=False)

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
