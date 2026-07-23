from collections import defaultdict, OrderedDict

from sqlalchemy.orm import Session

from app.data.ingredient_categories import COMMON_INGREDIENTS
from app.models import (
    MealPlan,
    ShoppingList,
    ShoppingListItem
)


def create_draft_shopping_list(db: Session, meal_plan: MealPlan):
    shopping_list = ShoppingList(meal_plan_id=meal_plan.id, status="draft")

    db.add(shopping_list)
    db.flush()

    items = defaultdict(lambda: {
        "name": "",
        "quantity": 0,
        "unit": ""
    })

    for plan_item in meal_plan.meal_plan_items:

        recipe = plan_item.recipe

        for ri in recipe.recipe_ingredients:

            ingredient_id = ri.ingredient_id

            if not items[ingredient_id]["name"]:
                items[ingredient_id]["name"] = ri.ingredient.name
                items[ingredient_id]["unit"] = ri.unit

            items[ingredient_id]["quantity"] += ri.quantity

    for ingredient_id, item in items.items():
        db.add(
            ShoppingListItem(
                shopping_list_id=shopping_list.id,
                ingredient_id=ingredient_id,
                quantity=item["quantity"],
                unit=item["unit"]
            )
        )

    db.commit()
    db.refresh(shopping_list)

    return shopping_list


def get_draft_shopping_list(db: Session, meal_plan_id: int):
    return (
        db.query(ShoppingList)
        .filter(
            ShoppingList.meal_plan_id == meal_plan_id,
            ShoppingList.status == "draft"
        )
        .first()
    )


def get_shopping_list(db: Session, meal_plan_id: int):
    return (
        db.query(ShoppingList)
        .filter(
            ShoppingList.meal_plan_id == meal_plan_id
        )
        .first()
    )


def update_shopping_list_item(db: Session, item_id: int, quantity: float, unit: str, note: str):
    item = (
        db.query(ShoppingListItem)
        .filter(ShoppingListItem.id == item_id)
        .first()
    )

    if not item:
        return None

    item.quantity = quantity
    item.unit = unit
    item.note = note

    db.commit()
    db.refresh(item)

    return item


def delete_shopping_list_item(db: Session, item):
    db.delete(item)
    db.commit()


def add_manual_item(db: Session, shopping_list_id: int, manual_name: str):
    item = ShoppingListItem(
        shopping_list_id=shopping_list_id,
        manual_name=manual_name.strip()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


def finalize_shopping_list(db: Session, meal_plan_id: int):
    shopping_list = get_shopping_list(
        db,
        meal_plan_id
    )

    if not shopping_list:
        return None

    shopping_list.status = "final"

    db.commit()
    db.refresh(shopping_list)

    return shopping_list


def get_grouped_shopping_list(shopping_list: ShoppingList):
    grouped_items = OrderedDict({
        "Grãos e Cereais": [],
        "Carnes e Proteínas": [],
        "Laticínios": [],
        "Legumes": [],
        "Verduras e Folhas": [],
        "Frutas": [],
        "Temperos e Condimentos": [],
        "Conservas": [],
        "Sementes e Oleaginosas": [],
        "Doces e Panificação": [],
        "Outros": []
    })

    for item in shopping_list.shopping_list_items:

        if item.manual_name:
            grouped_items["Outros"].append(item)
            continue

        category = get_ingredient_category(item.ingredient.name)

        if category not in grouped_items:
            grouped_items[category] = []

        grouped_items[category].append(item)

    return grouped_items


def get_ingredient_category(ingredient_name: str):
    for category, ingredients in COMMON_INGREDIENTS.items():

        if ingredient_name in ingredients:
            return category

    return "Outros"


def generate_shopping_list_text(shopping_list, checklist=False):
    lines = []

    # Lista formatada
    if not checklist:
        lines.append("🛒 Lista de Compras\n")

    grouped_items = get_grouped_shopping_list(shopping_list)

    for category, items in grouped_items.items():

        if not checklist:
            lines.append(
                f"\n{category}\n"
            )

        for item in items:

            if item.manual_name:
                name = item.manual_name

            else:
                name = item.ingredient.name

            quantity = ""

            if item.quantity and item.unit:
                quantity = (
                    f" - {item.quantity:g}{item.unit}"
                )

            note = ""

            if item.note:
                note = (
                    f" ({item.note})"
                )

            if checklist:
                lines.append(
                    f"☐ {name}{quantity}{note}"
                )

            else:
                lines.append(
                    f"• {name}{quantity}{note}"
                )

    return "\n".join(lines)


def refresh_shopping_list(db: Session, shopping_list: ShoppingList):
    meal_plan = shopping_list.meal_plan

    # ============================================
    # Gera a nova lista em memória
    # ============================================

    items = defaultdict(lambda: {
        "name": "",
        "quantity": 0,
        "unit": ""
    })

    for plan_item in meal_plan.meal_plan_items:

        recipe = plan_item.recipe

        for ri in recipe.recipe_ingredients:

            ingredient_id = ri.ingredient_id

            if not items[ingredient_id]["name"]:
                items[ingredient_id]["name"] = ri.ingredient.name
                items[ingredient_id]["unit"] = ri.unit

            items[ingredient_id]["quantity"] += ri.quantity

    # ============================================
    # Sincroniza com os itens atuais
    # ============================================

    current_items = list(shopping_list.shopping_list_items)

    print("==========")

    print("Shopping List")
    for item in current_items:
        print(
            f"{item.ingredient_id} | {item.quantity} | {item.manual_name} | {item.note}"
        )

    print()

    print("Nova Lista")
    for ingredient_id, item in items.items():
        print(
            f"{ingredient_id} | {item['quantity']}"
        )

    for current_item in current_items:

        # Nunca mexer em itens adicionados manualmente
        if current_item.manual_name:
            continue

        ingredient_id = current_item.ingredient_id

        if ingredient_id in items:

            # Atualiza quantidade
            current_item.quantity = items[ingredient_id]["quantity"]
            current_item.unit = items[ingredient_id]["unit"]

            # Remove do dicionário para sobrar apenas os novos
            items.pop(ingredient_id)

        else:

            # Não existe mais no planejamento
            db.delete(current_item)

    # ============================================
    # Adiciona ingredientes novos
    # ============================================

    for ingredient_id, item in items.items():
        db.add(
            ShoppingListItem(
                shopping_list_id=shopping_list.id,
                ingredient_id=ingredient_id,
                quantity=item["quantity"],
                unit=item["unit"]
            )
        )

    db.commit()

    db.refresh(shopping_list)

    updated_items = (
        db.query(ShoppingListItem)
        .filter(
            ShoppingListItem.shopping_list_id == shopping_list.id
        )
        .all()
    )

    print("==========")
    print("RESULTADO FINAL")

    for item in updated_items:
        print(
            f"{item.ingredient_id} | {item.quantity} | {item.manual_name} | {item.note}"
        )

    return shopping_list
