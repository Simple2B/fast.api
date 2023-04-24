from fastapi import Depends, HTTPException, status


from sqlalchemy.orm import Session


from app.database import get_db
from app.logger import log
import app.model as m


def get_current_post(
    post_uuid: str,
    db: Session = Depends(get_db),
) -> m.Post:
    post = db.query(m.Post).filter_by(uuid=post_uuid).first()
    if not post:
        log(log.WARNING, "Post %s not found", post_uuid)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post
