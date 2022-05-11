from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.services import AuthService, get_current_user
from app.serializers import UserCreate, User, Token

router = APIRouter(prefix="/auth")


@router.post("/sign_up", response_model=User)
async def sign_up(user_data: UserCreate):
    service = AuthService()
    return await service.register_new_user(user_data)


@router.post("/sign_in", response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    service = AuthService()
    return await service.authenticate_user(form_data.username, form_data.password)


@router.get("/user", response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user
