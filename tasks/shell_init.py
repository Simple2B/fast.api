# flake8: noqa F401
from app import model as m
from app.database import SessionLocal

db = SessionLocal()
