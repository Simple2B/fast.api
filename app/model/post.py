# pyright: reportUndefinedVariable=none
from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.database import db
from app.utils import generate_uuid


class Post(db.Model):
    __tablename__ = "posts"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)

    uuid: orm.Mapped[str] = orm.mapped_column(sa.String(36), default=generate_uuid)

    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("users.id"))
    title: orm.Mapped[str] = orm.mapped_column(sa.String(64), nullable=False)
    content: orm.Mapped[str] = orm.mapped_column(sa.String(512), nullable=False)
    is_published: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, default=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, default=datetime.now
    )

    user: orm.Mapped["User"] = orm.relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"<{self.id}: {self.title} at {self.created_at}>"
