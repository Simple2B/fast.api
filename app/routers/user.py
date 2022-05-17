from fastapi import HTTPException, Depends, APIRouter
from app import hash_utils, models, schemas, oauth2
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schemas.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user
