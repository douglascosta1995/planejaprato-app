from sqlalchemy.orm import Session

from app.models.recipe import Recipe
from app.models.recipe_ingredient import RecipeIngredient


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
    return db.query(Recipe).filter(Recipe.user_id == user_id).all()


def get_recipe_by_id(db, recipe_id):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def delete_recipe(db, recipe):
    db.delete(recipe)
    db.commit()
