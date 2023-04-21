from datetime import datetime, timedelta
from fastapi import status
from jose import JWTError, jwt
from fastapi import HTTPException

import app.schema as s
from app.config import Settings, get_settings

settings: Settings = get_settings()

SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> s.TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY)
        id: str = payload.get("user_id")

        if not id:
            raise credentials_exception

        token_data = s.TokenData(user_id=id)
    except JWTError:
        raise credentials_exception

    return token_data
