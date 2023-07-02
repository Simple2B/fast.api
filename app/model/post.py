from datetime import datetime
import sqlalchemy as sa
import sqlalchemy.orm as orm

from app.database import db
from app.utils import generate_uuid


class Post(db.Model):
    __tablename__ = "posts"

    id = sa.Column(sa.Integer, primary_key=True)

    uuid = sa.Column(sa.String(36), default=generate_uuid)

    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id"))

    title = sa.Column(sa.String(64), nullable=False)
    content = sa.Column(sa.String(512), nullable=False)
    is_published = sa.Column(sa.Boolean, default=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)

    user = orm.relationship("User", viewonly=True)

    def __repr__(self) -> str:
        return f"<{self.id}: {self.title} at {self.created_at}>"
