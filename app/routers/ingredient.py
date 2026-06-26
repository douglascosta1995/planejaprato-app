from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.ingredient import Ingredient

import unicodedata


def normalize(text: str):
    return ''.join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    ).lower()


router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/search")
def search_ingredients(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    normalized_query = normalize(q)

    ingredients = db.query(Ingredient).all()

    results = [
        ingredient
        for ingredient in ingredients
        if normalized_query in normalize(ingredient.name)
    ]

    return [
        {"id": i.id, "name": i.name}
        for i in results
    ]
