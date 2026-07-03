from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import RecipeCategory, Category
from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient


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


def delete_recipe(db, recipe):
    db.delete(recipe)
    db.commit()


def search_recipes(db: Session, user_id: int, query: str, meal_type: str | None = None):

    recipes = (db.query(Recipe).filter(
            Recipe.user_id == user_id,
            func.lower(Recipe.name).contains(query.lower())
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

    return (
        recipes
        .order_by(Recipe.name)
        .limit(20)
        .all()
    )
