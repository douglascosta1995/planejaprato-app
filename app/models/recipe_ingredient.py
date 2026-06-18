from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.database.database import Base


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    recipe_id = Column(
        Integer,
        ForeignKey("recipes.id"),
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
        String(50),
        nullable=False
    )
