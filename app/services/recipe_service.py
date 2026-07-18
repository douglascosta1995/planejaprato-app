from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models import RecipeCategory, Category, RecipeMealRole, MealRole
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient
from app.utils.text import normalize

MEAL_TYPE_TO_CATEGORY = {
    "breakfast": "Café da manhã",
    "lunch": "Almoço",
    "snack": "Lanche",
    "dinner": "Jantar"
}


def create_recipe(db: Session, name: str, instructions: str, user_id: int, ingredient_ids, quantities, units):
    recipe = Recipe(name=name, instructions=instructions, user_id=user_id)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    for ingredient_id, quantity, unit in zip(ingredient_ids, quantities, units):
        recipe_ingredient = RecipeIngredient(
            recipe_id=recipe.id,
            ingredient_id=ingredient_id,
            quantity=quantity,
            unit=unit
        )

        db.add(recipe_ingredient)

    db.commit()

    return recipe


def get_recipes_by_user(db, user_id):
    return db.query(Recipe).filter(Recipe.user_id == user_id, Recipe.is_system == False).all()


def get_system_recipes(db):
    return db.query(Recipe).filter(Recipe.is_system == True).all()


def get_recipe_by_id(db, recipe_id):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def count_user_recipes(db: Session, user_id: int) -> int:
    return (
        db.query(func.count(Recipe.id))
        .filter(Recipe.user_id == user_id)
        .scalar()
    )


def count_system_recipes(db: Session) -> int:
    return (
        db.query(func.count(Recipe.id))
        .filter(Recipe.is_system == True)
        .scalar()
    )


def delete_recipe(db, recipe):
    db.delete(recipe)
    db.commit()


def search_recipes(db: Session, user_id: int, query: str, meal_type: str | None = None):
    normalized_query = normalize(query)

    recipes = (
        db.query(Recipe)
        .filter(
            or_(
                Recipe.user_id == user_id,
                Recipe.is_system == True
            )
        )
    )

    if meal_type:

        category_name = MEAL_TYPE_TO_CATEGORY.get(meal_type)

        recipes = (
            recipes
            .join(RecipeCategory)
            .join(Category)
            .filter(Category.name == category_name)
        )

    recipes = recipes.order_by(Recipe.name).all()

    results = [

        recipe

        for recipe in recipes

        if normalized_query in normalize(recipe.name)

    ]

    return results[:20]


def get_recipes_by_role(
    db,
    user_id: int,
    category_name: str,
    role_name: str
):
    return (
        db.query(Recipe)
        .join(RecipeCategory)
        .join(Category)
        .join(RecipeMealRole)
        .join(MealRole)
        .filter(
            Category.name == category_name,
            MealRole.name == role_name,
            or_(
                Recipe.user_id == user_id,
                Recipe.is_system == True
            )
        )
        .all()
    )
