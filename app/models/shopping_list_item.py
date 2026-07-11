from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database.database import Base


class ShoppingListItem(Base):
    __tablename__ = "shopping_list_items"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    shopping_list_id = Column(
        Integer,
        ForeignKey("shopping_lists.id"),
        nullable=False
    )

    ingredient_id = Column(
        Integer,
        ForeignKey("ingredients.id"),
        nullable=False
    )

    quantity = Column(
        Float,
        nullable=False
    )

    unit = Column(
        String(20),
        nullable=False
    )

    note = Column(
        String(255),
        nullable=True
    )

    shopping_list = relationship(
        "ShoppingList",
        back_populates="shopping_list_items"
    )

    ingredient = relationship(
        "Ingredient"
    )

