from sqlalchemy.orm import Session

from app.models.recipe import Recipe


def create_recipe(db: Session, name: str, instructions: str, user_id: int):
    recipe = Recipe(name=name, instructions=instructions, user_id=user_id)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe


def get_recipes_by_user(db, user_id):
    return db.query(Recipe).filter(Recipe.user_id == user_id).all()


def get_recipe_by_id(db, recipe_id):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()


def delete_recipe(db, recipe):
    db.delete(recipe)
    db.commit()
