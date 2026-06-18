from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient


def get_ingredient_by_name(db: Session, name: str):
    return db.query(Ingredient).filter(Ingredient.name == name.strip().lower()).first()


def create_ingredient(db: Session, name: str):
    ingredient = Ingredient(name=name.strip().lower())

    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)

    return ingredient


def get_all_ingredients(db: Session):
    return db.query(Ingredient).order_by(Ingredient.name).all()
