import random
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import (
    MealPlan,
    MealPlanItem,
    Recipe,
    Category,
    RecipeCategory
)

from collections import defaultdict

DAYS = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo"
]


BREAKFAST = "Café da manhã"
LUNCH = "Almoço"
SNACK = "Lanche"
DINNER = "Jantar"


def generate_meal_plan(db: Session, user_id: int):

    breakfasts = get_recipes_by_category(db, user_id, BREAKFAST)

    lunches = get_recipes_by_category(db, user_id, LUNCH)

    snacks = get_recipes_by_category(db, user_id, SNACK)

    dinners = get_recipes_by_category(db, user_id, DINNER)

    if not breakfasts:
        return None

    if not lunches:
        return None

    if not snacks:
        return None

    if not dinners:
        return None

    meal_plan = MealPlan(
        name=f"Semana de {datetime.today().strftime('%d/%m/%Y')}",
        user_id=user_id
    )

    db.add(meal_plan)

    db.flush()

    for day in DAYS:

        add_meal(db, meal_plan.id, day, "breakfast", random.choice(breakfasts))

        add_meal(db, meal_plan.id, day, "lunch", random.choice(lunches))

        add_meal(db, meal_plan.id, day, "snack", random.choice(snacks))

        add_meal(db, meal_plan.id, day, "dinner", random.choice(dinners))

    db.commit()

    db.refresh(meal_plan)

    return meal_plan


def add_meal(db: Session, meal_plan_id: int, day: str, meal_type: str, recipe: Recipe):

    db.add(

        MealPlanItem(
            meal_plan_id=meal_plan_id,
            day_of_week=day,
            meal_type=meal_type,
            recipe_id=recipe.id
        )

    )


def get_recipes_by_category(db: Session, user_id: int, category_name: str):

    category = (
        db.query(Category)
        .filter(Category.name == category_name)
        .first()
    )

    if not category:
        return []

    return (
        db.query(Recipe)
        .join(RecipeCategory)
        .filter(
            Recipe.user_id == user_id,
            RecipeCategory.category_id == category.id
        )
        .all()
    )


def get_meal_plan_by_id(db: Session, meal_plan_id: int):

    return (
        db.query(MealPlan)
        .filter(MealPlan.id == meal_plan_id)
        .first()
    )


def get_user_meal_plans(db: Session, user_id: int):

    return (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc())
        .all()
    )


def delete_meal_plan(db: Session, meal_plan: MealPlan):

    db.delete(meal_plan)
    db.commit()


def organize_meal_plan(meal_plan):

    days = {}

    for item in meal_plan.meal_plan_items:

        if item.day_of_week not in days:
            days[item.day_of_week] = {}

        days[item.day_of_week][item.meal_type] = item

    return days


def get_user_latest_meal_plan(db: Session, user_id: int):

    return (
        db.query(MealPlan)
        .filter(MealPlan.user_id == user_id)
        .order_by(MealPlan.created_at.desc())
        .first()
    )


def generate_shopping_list(meal_plan):
    """
    Versão 1: soma simples de ingredientes
    """

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

    return items
