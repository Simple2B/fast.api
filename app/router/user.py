from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from app.dependency import get_current_user
from app.database import get_db

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=s.UserOut)
def create_user(user: s.UserCreate, db: Session = Depends(get_db)):
    new_user = m.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=s.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    user = db.query(m.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user
