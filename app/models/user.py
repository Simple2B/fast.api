from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.now)
