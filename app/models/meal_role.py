from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class MealRole(Base):
    __tablename__ = "meal_roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    recipe_meal_roles = relationship(
        "RecipeMealRole",
        back_populates="meal_role",
        cascade="all, delete-orphan"
    )
