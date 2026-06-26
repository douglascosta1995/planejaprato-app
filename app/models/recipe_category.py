from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class RecipeCategory(Base):
    __tablename__ = "recipe_categories"

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

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False
    )

    recipe = relationship(
        "Recipe",
        back_populates="recipe_categories"
    )

    category = relationship(
        "Category",
        back_populates="recipe_categories"
    )
