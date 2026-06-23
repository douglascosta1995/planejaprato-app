from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models.ingredient import Ingredient

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/search")
def search_ingredients(q: str = Query(..., min_length=1), db: Session = Depends(get_db)):
    results = db.query(Ingredient).filter(Ingredient.name.ilike(f"%{q}%")).limit(10).all()

    return [
        {"id": i.id, "name": i.name}
        for i in results
    ]
