from fastapi import FastAPI
from app.router import post, user, auth
from .config import settings

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root():
    SAMPLE_ENV_VAR = settings.SAMPLE_ENV_VAR
    return {"ENV": SAMPLE_ENV_VAR}
