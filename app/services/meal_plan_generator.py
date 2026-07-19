import random

from app.services.recipe_service import get_recipes_by_role
from app.utils.meal_templates import MEAL_TEMPLATES

# templates
'''BREAKFAST_TEMPLATES = [

    {
        "name": "Pão com Proteína",
        "roles": ["Pão", "Proteína", "Fruta"]
    },

    {
        "name": "Cuscuz",
        "roles": ["Cuscuz", "Proteína"]
    },

    {
        "name": "Vitamina",
        "roles": ["Fruta"]
    },

    {
        "name": "Aveia",
        "roles": ["Aveia", "Fruta"]
    }

]

LUNCH_TEMPLATES = [

    {
        "name": "Tradicional",
        "weight": 60,
        "roles": ["Arroz", "Feijão", "Proteína", "Salada"]
    },

    {
        "name": "Massa",
        "weight": 20,
        "roles": ["Massa", "Proteína", "Salada"]
    },

    {
        "name": "Purê",
        "weight": 10,
        "roles": ["Purê", "Proteína", "Salada"]
    },

    {
        "name": "Prato Único",
        "weight": 10,
        "roles": ["Prato Único"]
    }

]

DINNER_TEMPLATES = [

    {
        "name": "Jantar Tradicional",
        "roles": ["Arroz", "Proteína", "Salada"]
    },

    {
        "name": "Massa",
        "roles": ["Massa", "Proteína"]
    },

    {
        "name": "Prato Único",
        "roles": ["Prato Único"]
    },

    {
        "name": "Jantar Leve",
        "roles": ["Salada", "Proteína"]
    }

]

SNACK_TEMPLATES = [

    {
        "name": "Fruta",
        "roles": ["Fruta"]
    },

    {
        "name": "Iogurte",
        "roles": ["Iogurte", "Fruta"]
    },

    {
        "name": "Pão",
        "roles": ["Pão", "Proteína"]
    },

    {
        "name": "Cuscuz",
        "roles": ["Cuscuz"]
    }

]
'''

def pick_recipe(recipes):
    recipe = random.choice(recipes)

    return recipe


def generate_lunch(db, user_id):
    lunch = []

    # Carboidrato (obrigatório)
    carbs = get_recipes_by_role(
        db=db,
        user_id=user_id,
        category_name="Almoço",
        role_name="Carboidrato"
    )

    if carbs:
        lunch.append(
            pick_recipe(carbs)
        )

    # Proteína (obrigatória)
    proteins = get_recipes_by_role(
        db=db,
        user_id=user_id,
        category_name="Almoço",
        role_name="Proteína"
    )

    if proteins:
        lunch.append(
            pick_recipe(proteins)
        )

    # Verdura (opcional)
    greens = get_recipes_by_role(
        db=db,
        user_id=user_id,
        category_name="Almoço",
        role_name="Verdura"
    )

    if greens:
        lunch.append(
            pick_recipe(greens)
        )

    # Legume (opcional)
    vegetables = get_recipes_by_role(
        db=db,
        user_id=user_id,
        category_name="Almoço",
        role_name="Legume"
    )

    if vegetables:
        lunch.append(
            pick_recipe(vegetables)
        )

    return lunch


def generate_meal_plan(db, user_id):
    breakfast = generate_meal_from_template(
        db=db,
        user_id=user_id,
        category_name="Café da manhã",
        templates=MEAL_TEMPLATES["Café da manhã"]
    )

    lunch = generate_meal_from_template(
        db=db,
        user_id=user_id,
        category_name="Almoço",
        templates=MEAL_TEMPLATES["Almoço"]
    )

    snack = generate_meal_from_template(
        db=db,
        user_id=user_id,
        category_name="Lanche",
        templates=MEAL_TEMPLATES["Lanche"]
    )

    dinner = generate_meal_from_template(
        db=db,
        user_id=user_id,
        category_name="Jantar",
        templates=MEAL_TEMPLATES["Jantar"]
    )

    return {
        "breakfast": breakfast,
        "lunch": lunch,
        "snack": snack,
        "dinner": dinner
    }


def generate_meal_from_template(db, user_id, category_name, templates):
    template = random.choices(
        templates,
        weights=[t.get("weight", 1) for t in templates],
        k=1
    )[0]

    recipes = []

    for role in template["roles"]:

        options = get_recipes_by_role(
            db=db,
            user_id=user_id,
            category_name=category_name,
            role_name=role
        )

        if not options:
            print(f"Nenhuma receita encontrada para o MealRole: {role}")
            return None

        recipe = pick_recipe(options)

        recipes.append(recipe)

    return {
        "template": template["name"],
        "recipes": recipes
    }
