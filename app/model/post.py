from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
