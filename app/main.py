import jinja2

# patch https://jinja.palletsprojects.com/en/3.0.x/changes/
# pass_context replaces contextfunction and contextfilter.
jinja2.contextfunction = jinja2.pass_context
# flake8: noqa F402

from fastapi import FastAPI

# from sqladmin import Admin

from app.router import router

# from app import admin
# from app.admin import authentication_backend
from app.database import db

app = FastAPI()

# admin = Admin(
#     app=app,
#     authentication_backend=authentication_backend,
#     engine=db.Session,
#     templates_dir="app/templates/admin",
# )

# sql_admin = Admin(app, engine)

app.include_router(router)


@app.get("/")
def root():
    return {"message": "Hello"}
