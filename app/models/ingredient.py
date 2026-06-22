from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base
from sqlalchemy.orm import relationship


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    recipe_ingredients = relationship(
        "RecipeIngredient",
        back_populates="ingredient"
    )
