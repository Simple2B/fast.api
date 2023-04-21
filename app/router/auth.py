# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
import app.model as m
import app.schema as s
from app.oauth2 import create_access_token

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/login", response_model=s.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user: m.User = m.User.authenticate(
        db,
        user_credentials.username,  # its email
        user_credentials.password,
    )

    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return s.Token(
        access_token=access_token,
        token_type="Bearer",
    )
