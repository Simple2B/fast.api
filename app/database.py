from functools import lru_cache
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

from app.config import get_settings, Settings

settings: Settings = get_settings()

DB_URI = settings.DATABASE_URI if settings.DATABASE_URI else settings.DEV_DATABASE_URI

engine = create_engine(DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@lru_cache
def get_engine() -> Engine:
    settings: Settings = get_settings()
    return create_engine(settings.DB_URI)


def get_db() -> Generator[Session, None, None]:
    engine: Engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
