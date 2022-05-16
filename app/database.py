from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from app.config import settings

DB_URI = settings.DATABASE_URI if settings.DATABASE_URI else settings.DEV_DATABASE_URI

engine = create_engine(DB_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base.query = db_session.query_property()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
