from sqlalchemy import Column, Text, Boolean
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime

from datetime import datetime

from app.database.database import Base
from sqlalchemy.orm import relationship


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    is_system = Column(
        Boolean,
        default=False,
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(
        String(150),
        nullable=False
    )

    instructions = Column(
        Text,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    recipe_ingredients = relationship(
        "RecipeIngredient",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    recipe_categories = relationship(
        "RecipeCategory",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )

    meal_plan_items = relationship(
        "MealPlanItem",
        back_populates="recipe"
    )

    recipe_meal_roles = relationship(
        "RecipeMealRole",
        back_populates="recipe",
        cascade="all, delete-orphan"
    )
