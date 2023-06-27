from sqlalchemy import Column, Integer, String
from app.database import Base


class GroceryItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String(24))
    quantity = Column(Integer)
    category = Column(String(64), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.id}: {self.name} ({self.quantity}) {self.category}>"
