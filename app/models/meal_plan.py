from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.database.database import Base


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id = Column(
        Integer,
        primary_key=True,
        index=True
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

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    user = relationship(
        "User"
    )

    meal_plan_items = relationship(
        "MealPlanItem",
        back_populates="meal_plan",
        cascade="all, delete-orphan"
    )
