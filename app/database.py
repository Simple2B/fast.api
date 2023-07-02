# from functools import lru_cache
from typing import Generator
from alchemical import Alchemical
from sqlalchemy import orm

from app.config import get_settings, Settings

settings: Settings = get_settings()

DB_URI = settings.DATABASE_URI if settings.DATABASE_URI else settings.DEV_DATABASE_URI

db = Alchemical(DB_URI)


def get_db() -> Generator[orm.Session, None, None]:
    with db.Session() as session:
        yield session
