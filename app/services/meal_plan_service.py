import random
from datetime import datetime

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import (
    MealPlan,
    MealPlanItem,
    Recipe,
    Category,
    RecipeCategory
)

from collections import defaultdict
from app.services.meal_plan_generator import (
    generate_meal_from_template,
    BREAKFAST_TEMPLATES,
    LUNCH_TEMPLATES,
    SNACK_TEMPLATES,
    DINNER_TEMPLATES
)

DAYS = [
    "Segunda",
    "Terça",
    "Quarta",
    "Quinta",
    "Sexta",
    "Sábado",
    "Domingo"
]


def generate_meal_plan(db: Session, user_id: int):

    meal_plan = MealPlan(
        name=f"Semana de {datetime.today().strftime('%d/%m/%Y')}",
        user_id=user_id
    )

    db.add(meal_plan)

    db.flush()

    for day in DAYS:

        breakfast = generate_meal_from_template(
            db,
            user_id,
            "Café da manhã",
            BREAKFAST_TEMPLATES
        )

        lunch = generate_meal_from_template(
            db,
            user_id,
            "Almoço",
            LUNCH_TEMPLATES
        )

        snack = generate_meal_from_template(
            db,
            user_id,
            "Lanche",
            SNACK_TEMPLATES
        )

        dinner = generate_meal_from_template(
            db,
            user_id,
            "Jantar",
            DINNER_TEMPLATES
            )

        if not breakfast or not lunch or not snack or not dinner:
            return None

        add_meal(db, meal_plan.id, day, "breakfast", breakfast["recipes"])
        add_meal(db, meal_plan.id, day, "lunch", lunch["recipes"])
        add_meal(db, meal_plan.id, day, "snack", snack["recipes"])
        add_meal(db, meal_plan.id, day, "dinner", dinner["recipes"])

    db.commit()

    db.refresh(meal_plan)

    return meal_plan


def add_meal(db: Session, meal_plan_id: int, day: str, meal_type: str, recipes):

    for recipe in recipes:

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
            RecipeCategory.category_id == category.id,
            or_(
                Recipe.user_id == user_id,
                Recipe.is_system == True
            )
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

    # Sempre cria todos os dias
    for day in DAYS:

        days[day] = {
            "breakfast": [],
            "lunch": [],
            "snack": [],
            "dinner": []
        }

    # Adiciona todas as receitas
    for item in meal_plan.meal_plan_items:

        days[item.day_of_week][item.meal_type].append(item)

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


def add_meal_plan_item(db: Session, meal_plan_id: int, day: str, meal_type: str, recipe_id: int):

    meal = MealPlanItem(
        meal_plan_id=meal_plan_id,
        day_of_week=day,
        meal_type=meal_type,
        recipe_id=recipe_id
    )

    db.add(meal)

    db.commit()

    db.refresh(meal)

    return meal


def replace_meal_plan_item(db: Session, item_id: int, recipe_id: int):

    item = (
        db.query(MealPlanItem)
        .filter(MealPlanItem.id == item_id)
        .first()
    )

    if not item:
        return None

    item.recipe_id = recipe_id

    db.commit()
    db.refresh(item)

    return item
