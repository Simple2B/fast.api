import jinja2 
 
# patch https://jinja.palletsprojects.com/en/3.0.x/changes/ 
# pass_context replaces contextfunction and contextfilter. 
jinja2.contextfunction = jinja2.pass_context 
# flake8: noqa F402

from fastapi import FastAPI
from sqladmin import Admin, ModelView

from app.router import post, user, auth
from app import admin
from app.database import engine
from .config import settings


app = FastAPI()

sql_admin = Admin(app, engine)

sql_admin.add_view(admin.user.UserAdmin)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    SAMPLE_ENV_VAR = settings.SAMPLE_ENV_VAR
    return {"ENV": SAMPLE_ENV_VAR}
