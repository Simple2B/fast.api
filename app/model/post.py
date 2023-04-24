from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base
from app.utils import generate_uuid


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    uuid = Column(String(36), default=generate_uuid)

    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String(64), nullable=False)
    content = Column(String(512), nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", viewonly=True)

    def __repr__(self) -> str:
        return f"<{self.id}: {self.title} at {self.created_at}>"
