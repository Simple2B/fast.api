from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.logger import log
import app.model as m
import app.schema as s
from app.database import get_db
from app.dependency import get_current_user, get_current_post


post_router = APIRouter(prefix="/post", tags=["Posts"])


@post_router.post("/", status_code=status.HTTP_201_CREATED, response_model=s.Post)
def create_posts(
    post: s.BasePost,
    db: Session = Depends(get_db),
    current_user: m.User = Depends(get_current_user),
):
    new_post = m.Post(
        title=post.title,
        content=post.content,
        is_published=post.published,
        user_id=current_user.id,
    )
    db.add(new_post)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.INFO, "Error creating a new post - %s", e)
    log(log.INFO, "Post created successfully")
    return new_post


@post_router.get("/posts", response_model=s.PostList)
def get_posts(
    db: Session = Depends(get_db),
):
    posts = db.query(m.Post).all()
    return s.PostList(posts=posts)


@post_router.get("/{post_uuid}", response_model=s.Post)
def get_post(
    post_uuid: str,
    post: m.Post = Depends(get_current_post),
    current_user: m.User = Depends(get_current_user),
):
    if post not in current_user.posts:
        log(log.ERROR, "Post %s does not belong to the current user", post_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post for this user not found"
        )
    return post


@post_router.put("/{post_uuid}", response_model=s.Post)
def update_post(
    post_uuid: str,
    post_data: s.BasePost,
    db: Session = Depends(get_db),
    post: m.Post = Depends(get_current_post),
    current_user: m.User = Depends(get_current_user),
):
    if post not in current_user.posts:
        log(log.ERROR, "Post %s does not belong to the current user", post_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post for this user not found"
        )
    post.title = post_data.title
    post.content = post_data.content
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Post has not been updated - %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error updating post"
        )
    log(log.INFO, "Post updated successfully")
    return post


@post_router.delete("/{post_uuid}", status_code=status.HTTP_200_OK)
def delete_post(
    post_uuid: str,
    db: Session = Depends(get_db),
    post: m.Post = Depends(get_current_post),
    current_user: m.User = Depends(get_current_user),
):
    if post not in current_user.posts:
        log(log.ERROR, "Post %s does not belong to the current user", post_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post for this user not found"
        )
    db.delete(post)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Error while deleting post - %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error while deleting post"
        )
    return status.HTTP_200_OK
