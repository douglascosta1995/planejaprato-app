from sqlalchemy.orm import Session

from app.models import MealRole

MEAL_ROLES = [
    "Arroz",
    "Feijão",
    "Proteína",
    "Massa",
    "Purê",
    "Salada",
    "Prato Único",
    "Pão",
    "Fruta",
    "Aveia",
    "Cuscuz",
    "Iogurte"
]


def populate_meal_roles(db: Session):

    for role_name in MEAL_ROLES:

        exists = (
            db.query(MealRole)
            .filter(MealRole.name == role_name)
            .first()
        )

        if exists:
            continue

        db.add(
            MealRole(
                name=role_name
            )
        )

    db.commit()
