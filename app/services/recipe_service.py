from sqlalchemy.orm import Session

from app.models.recipe import Recipe


def create_recipe(db: Session, name: str, instructions: str, user_id: int):
    recipe = Recipe(name=name, instructions=instructions, user_id=user_id)

    db.add(recipe)
    db.commit()
    db.refresh(recipe)

    return recipe
