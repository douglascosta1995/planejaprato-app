from collections import defaultdict

from sqlalchemy.orm import Session

from app.models import (
    MealPlan,
    ShoppingList,
    ShoppingListItem
)


def create_draft_shopping_list(db: Session, meal_plan: MealPlan):
    shopping_list = ShoppingList(meal_plan_id=meal_plan.id, status="draft")

    db.add(shopping_list)
    db.flush()

    items = defaultdict(lambda: {
        "name": "",
        "quantity": 0,
        "unit": ""
    })

    for plan_item in meal_plan.meal_plan_items:

        recipe = plan_item.recipe

        for ri in recipe.recipe_ingredients:

            ingredient_id = ri.ingredient_id

            if not items[ingredient_id]["name"]:
                items[ingredient_id]["name"] = ri.ingredient.name
                items[ingredient_id]["unit"] = ri.unit

            items[ingredient_id]["quantity"] += ri.quantity

    for ingredient_id, item in items.items():

        db.add(
            ShoppingListItem(
                shopping_list_id=shopping_list.id,
                ingredient_id=ingredient_id,
                quantity=item["quantity"],
                unit=item["unit"]
            )
        )

    db.commit()
    db.refresh(shopping_list)

    return shopping_list


def get_draft_shopping_list(db: Session, meal_plan_id: int):

    return (
        db.query(ShoppingList)
        .filter(
            ShoppingList.meal_plan_id == meal_plan_id,
            ShoppingList.status == "draft"
        )
        .first()
    )


def update_shopping_list_item(db: Session, item_id: int, quantity: float, unit: str, note: str):
    item = (
        db.query(ShoppingListItem)
        .filter(ShoppingListItem.id == item_id)
        .first()
    )

    if not item:
        return None

    item.quantity = quantity
    item.unit = unit
    item.note = note

    db.commit()
    db.refresh(item)

    return item


def delete_shopping_list_item(db: Session, item):

    db.delete(item)
    db.commit()


def add_manual_item(db: Session, shopping_list_id: int, manual_name: str):

    item = ShoppingListItem(
        shopping_list_id=shopping_list_id,
        manual_name=manual_name.strip()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item
