from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.logger import log
from app import schema, model
from app.database import get_db


shopping_item_router = APIRouter(prefix="/shopping", tags=["Items"])


@shopping_item_router.get("/items", response_model=schema.ItemsList)
def get_items(
    db: Session = Depends(get_db),
):
    items = db.query(model.GroceryItem).all()
    log(log.INFO, "Grocery items: %s", items)
    return schema.ItemsList(items=items)


@shopping_item_router.post(
    "/add",
    status_code=status.HTTP_201_CREATED,
    response_model=schema.GroceryItem,
)
def add_item(item: schema.GroceryItem, db: Session = Depends(get_db)):
    new_item = model.GroceryItem(
        name=item.name,
        quantity=item.quantity,
        category=item.category,
    )
    db.add(new_item)
    db.commit()
    log(log.INFO, "Item added: %s", new_item)
    return new_item


@shopping_item_router.delete(
    "/{item_id}",
    status_code=status.HTTP_200_OK,
)
def delete_post(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = db.query(model.GroceryItem).filter_by(id=item_id).first()
    db.delete(item)
    try:
        db.commit()
    except SQLAlchemyError as e:
        log(log.ERROR, "Error while deleting item - %s", e)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Error while deleting item"
        )
    return status.HTTP_200_OK
