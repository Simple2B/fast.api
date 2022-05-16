# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas import Token
from app.database import get_db
from app.models import User
from app.hash_utils import hash_verify
from app.oauth2 import create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(email=user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    if not hash_verify(user_credentials.password, user.password):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
