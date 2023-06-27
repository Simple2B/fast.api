from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app import model, schema


def test_items(
    client: TestClient,
    db: Session,
):
    TESTING_ITEMS_NUMBER = 3
    for i in range(TESTING_ITEMS_NUMBER):
        item = model.GroceryItem(
            name=f"Item_{i}",
            quantity=12,
            category="diary",
        )
        db.add(item)
        db.commit()

    response = client.get(
        "api/shopping/items",
    )
    assert response.status_code == 200
    assert db.query(model.GroceryItem).count() == TESTING_ITEMS_NUMBER


def test_add_items(
    client: TestClient,
    db: Session,
):
    data = schema.GroceryItem(
        name="Cheese",
        quantity=12,
        category="diary",
    )
    response = client.post("api/shopping/add", json=data.dict())
    assert response.status_code == 201


def test_delete_items(
    client: TestClient,
    db: Session,
):
    item = model.GroceryItem(
        name="item_to_delete",
        quantity=12,
        category="diary",
    )
    db.add(item)
    db.commit()

    item_to_delete = (
        db.query(model.GroceryItem).filter_by(name="item_to_delete").first()
    )
    assert item_to_delete.name == "item_to_delete"
    assert db.query(model.GroceryItem).count() == 1

    response = client.delete(f"api/shopping/{item_to_delete.id}")
    assert response.status_code == 200
    assert db.query(model.GroceryItem).count() == 0
