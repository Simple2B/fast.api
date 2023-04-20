from fastapi import HTTPException, Response, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session

import app.model as m
import app.schema as s
from app.database import get_db
from app.dependency import get_current_user


post_router = APIRouter(prefix="/posts", tags=["Posts"])


@post_router.get("/", response_model=List[s.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(m.Post).all()
    return posts


@post_router.post("/", status_code=201, response_model=s.Post)
def create_posts(
    post: s.BasePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = m.Post(
        title=post.title,
        content=post.content,
        published=post.published,
        user_id=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@post_router.get("/{id}", response_model=s.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(m.Post).get(id)
    if not post:
        raise HTTPException(status_code=404, detail="This post was not found")
    return post


@post_router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    deleted_post = db.query(m.Post).filter_by(id=id)
    if not deleted_post.first():
        raise HTTPException(status_code=404, detail="This post was not found")

    if deleted_post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)


@post_router.put("/{id}", response_model=s.Post)
def update_post(
    id: int,
    post: s.BasePost,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    updated_post = db.query(m.Post).filter_by(id=id)

    if not updated_post.first():
        raise HTTPException(status_code=404, detail="This post was not found")

    if updated_post.first().user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()

    return updated_post.first()
