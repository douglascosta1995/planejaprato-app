from sqlalchemy.orm import Session

from app.models import MealPlanItem


def get_meal_plan_item_by_id(db: Session, item_id: int):

    return (
        db.query(MealPlanItem)
        .filter(MealPlanItem.id == item_id)
        .first()
    )


def delete_meal_plan_item(db: Session, meal_plan_item: MealPlanItem):

    meal_plan_id = meal_plan_item.meal_plan_id

    db.delete(meal_plan_item)

    db.commit()

    return meal_plan_id
