from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    meal_plan_id = Column(
        Integer,
        ForeignKey("meal_plans.id"),
        nullable=False
    )

    status = Column(
        String(20),
        default="draft",
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    meal_plan = relationship(
        "MealPlan",
        back_populates="shopping_list"
    )

    shopping_list_items = relationship(
        "ShoppingListItem",
        back_populates="shopping_list",
        cascade="all, delete-orphan"
    )
