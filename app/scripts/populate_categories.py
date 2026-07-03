from sqlalchemy.orm import Session

from app.models.category import Category

CATEGORIES = [
    "Café da manhã",
    "Almoço",
    "Jantar",
    "Lanche"
]


def populate_categories(db: Session):

    count = 0

    for category_name in CATEGORIES:

        exists = (
            db.query(Category)
            .filter(Category.name == category_name)
            .first()
        )

        if exists:
            continue

        db.add(
            Category(
                name=category_name
            )
        )

        count += 1

    db.commit()

    print(f"{count} categorias adicionadas.")
