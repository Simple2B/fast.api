from fastapi import Depends, APIRouter, status
from sqlalchemy.orm import Session
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
