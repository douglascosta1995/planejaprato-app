from app.scripts.populate_categories import populate_categories
from app.scripts.populate_ingredients import populate_ingredients
from app.scripts.populate_meal_roles import populate_meal_roles
from app.scripts.populate_system_recipes import populate_system_recipes
from app.scripts.populate_system_user import populate_system_user


def initialize_database(db):

    system_user = populate_system_user(db)

    populate_ingredients(db)
    populate_categories(db)
    populate_meal_roles(db)
    populate_system_recipes(db, system_user)
