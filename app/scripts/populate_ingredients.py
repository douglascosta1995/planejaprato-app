from sqlalchemy.orm import Session

from app.data.ingredient_categories import COMMON_INGREDIENTS
from app.models.ingredient import Ingredient
from app.models.recipe_ingredient import RecipeIngredient


def populate_ingredients(db: Session):
    count = 0

    for category, ingredients in COMMON_INGREDIENTS.items():
        for ingredient_name in ingredients:

            exists = (
                db.query(Ingredient)
                .filter(Ingredient.name == ingredient_name)
                .first()
            )

            if not exists:
                db.add(
                    Ingredient(
                        name=ingredient_name
                    )
                )
                count += 1

    db.commit()

    print(f"{count} ingredientes adicionados.")
