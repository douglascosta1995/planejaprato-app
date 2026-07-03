import json

from sqlalchemy.orm import Session

from app.models import (
    Recipe,
    Ingredient,
    Category,
    MealRole,
    RecipeIngredient,
    RecipeCategory,
    RecipeMealRole,
    User
)


def populate_system_recipes(db: Session, system_user: User):

    with open(
        "app/data/system_recipes.json",
        encoding="utf-8"
    ) as file:

        recipes = json.load(file)

    created = 0

    for recipe_data in recipes:

        exists = (
            db.query(Recipe)
            .filter(Recipe.name == recipe_data["name"])
            .first()
        )

        if exists:
            continue

        recipe = Recipe(
            name=recipe_data["name"],
            instructions=recipe_data["instructions"],
            is_system=True,
            user_id=system_user.id
        )

        db.add(recipe)

        db.flush()

        #
        # Categories
        #

        for category_name in recipe_data["categories"]:

            category = (
                db.query(Category)
                .filter(Category.name == category_name)
                .first()
            )

            db.add(

                RecipeCategory(
                    recipe_id=recipe.id,
                    category_id=category.id
                )

            )

        #
        # Meal Roles
        #

        for role_name in recipe_data["meal_roles"]:

            role = (
                db.query(MealRole)
                .filter(MealRole.name == role_name)
                .first()
            )

            db.add(

                RecipeMealRole(
                    recipe_id=recipe.id,
                    meal_role_id=role.id
                )

            )

        #
        # Ingredients
        #

        for ingredient_data in recipe_data["ingredients"]:

            ingredient = (
                db.query(Ingredient)
                .filter(
                    Ingredient.name == ingredient_data["name"]
                )
                .first()
            )

            db.add(

                RecipeIngredient(

                    recipe_id=recipe.id,

                    ingredient_id=ingredient.id,

                    quantity=ingredient_data["quantity"],

                    unit=ingredient_data["unit"]

                )

            )

        created += 1

    db.commit()

    print(f"{created} receitas adicionadas.")
