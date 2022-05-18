from fastapi import HTTPException, Response, Depends, APIRouter
from typing import List
from app import model, oauth2, schema
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(model.Post).all()
    return posts


@router.post("/", status_code=201, response_model=schema.Post)
def create_posts(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = model.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        user_id=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(model.Post).get(id)
    if not post:
        raise HTTPException(status_code=404, detail="This post was not found")
    return post


@router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    deleted_post = db.query(model.Post).filter_by(id=id)
    if not deleted_post.first():
        raise HTTPException(status_code=404, detail="This post was not found")

    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


@router.put("/{id}", response_model=schema.Post)
def update_post(
    id: int,
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    updated_post = db.query(model.Post).filter_by(id=id)

    if not updated_post.first():
        raise HTTPException(status_code=404, detail="This post was not found")

    if updated_post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()
