from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class RecipeMealRole(Base):
    __tablename__ = "recipe_meal_roles"

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
        primary_key=True
    )

    meal_role_id = Column(
        Integer,
        ForeignKey("meal_roles.id"),
        primary_key=True
    )

    recipe = relationship(
        "Recipe",
        back_populates="recipe_meal_roles"
    )

    meal_role = relationship(
        "MealRole",
        back_populates="recipe_meal_roles"
    )
