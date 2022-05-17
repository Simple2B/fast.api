# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schema import Token
from app.database import get_db
from app.model import User
from app.oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user: User = User.authenticate(
        db,
        user_credentials.username,
        user_credentials.password,
    )

    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
