from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.schema import TokenData
from app.database import get_db
from app.model import User
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=404,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter_by(id=token.id).first()

    return user
