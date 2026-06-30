from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class MealPlanItem(Base):
    __tablename__ = "meal_plan_items"

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

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
        nullable=False
    )

    day_of_week = Column(
        String(20),
        nullable=False
    )

    meal_type = Column(
        String(30),
        nullable=False
    )

    meal_plan = relationship(
        "MealPlan",
        back_populates="meal_plan_items"
    )

    recipe = relationship(
        "Recipe",
        back_populates="meal_plan_items"
    )
