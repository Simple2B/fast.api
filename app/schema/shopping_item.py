from pydantic import BaseModel


class GroceryItem(BaseModel):
    name: str
    quantity: int
    category: str

    class Config:
        orm_mode = True


class ItemsList(BaseModel):
    items: list[GroceryItem]
