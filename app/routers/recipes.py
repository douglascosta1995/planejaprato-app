from typing import List

from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi import Depends
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.dependencies import get_current_user
from app.models import RecipeCategory, Category
from app.models.user import User

from app.services.recipe_service import create_recipe, get_recipe_by_id, delete_recipe, search_recipes
from app.utils.messages import MESSAGES

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/recipes/new")
def new_recipe(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="app/new_recipe.html",
        context={
            "user": current_user
        }
    )


@router.post("/recipes")
def create_recipe_route(name: str = Form(...), instructions: str = Form(""), ingredient_ids: List[int] = Form([]),
                        quantities: List[float] = Form([]), units: List[str] = Form([]),
                        current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe = create_recipe(db=db, name=name, instructions=instructions, user_id=current_user.id,
                           ingredient_ids=ingredient_ids,
                           quantities=quantities, units=units)

    return RedirectResponse(
        url=f"/recipes/{recipe.id}?message=recipe_created&highlight=categories",
        status_code=303
    )


@router.get("/recipes/search")
def search_recipes_route(q: str, meal_type: str | None = None, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    recipes = search_recipes(
        db=db,
        user_id=current_user.id,
        query=q,
        meal_type=meal_type
    )

    return [
        {
            "id": recipe.id,
            "name": recipe.name
        }
        for recipe in recipes
    ]


@router.get("/recipes/{recipe_id}")
def recipe_detail(recipe_id: int, request: Request, current_user: User = Depends(get_current_user),
                  db: Session = Depends(get_db)):
    recipe = get_recipe_by_id(db, recipe_id)

    if not recipe:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    if recipe.user_id != current_user.id:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    categories = db.query(Category).all()

    selected_categories = [rc.category_id for rc in recipe.recipe_categories]

    message_key = request.query_params.get("message")

    message = MESSAGES.get(message_key)

    highlight = request.query_params.get("highlight")

    return templates.TemplateResponse(
        request=request,
        name="app/recipe_detail.html",
        context={
            "user": current_user,
            "recipe": recipe,
            "categories": categories,
            "selected_categories": selected_categories,
            "message": message,
            "highlight": highlight
        }
    )


@router.post("/recipes/{recipe_id}/delete")
def delete_recipe_route(recipe_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    recipe = get_recipe_by_id(db, recipe_id)

    if not recipe:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    if recipe.user_id != current_user.id:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    delete_recipe(db, recipe)

    return RedirectResponse(
        "/dashboard?message=recipe_deleted",
        status_code=303
    )


@router.post("/recipes/{recipe_id}/categories/toggle")
def toggle_recipe_category(recipe_id: int, category_id: int = Form(...), db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    recipe = get_recipe_by_id(db, recipe_id)

    if not recipe or recipe.user_id != current_user.id:
        return {"success": False}

    existing = db.query(RecipeCategory).filter_by(
        recipe_id=recipe_id,
        category_id=category_id
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

        return {
            "success": True,
            "action": "removed"
        }

    db.add(
        RecipeCategory(
            recipe_id=recipe_id,
            category_id=category_id
        )
    )
    db.commit()

    return {
        "success": True,
        "action": "added"
    }
