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
from app.models.user import User

from app.services.recipe_service import create_recipe, get_recipe_by_id, delete_recipe

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
    create_recipe(db=db, name=name, instructions=instructions, user_id=current_user.id, ingredient_ids=ingredient_ids,
                  quantities=quantities, units=units)

    print("ingredient_ids:", ingredient_ids)
    print("quantities:", quantities)
    print("units:", units)

    return RedirectResponse(
        url="/dashboard?message=recipe_created",
        status_code=303
    )


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

    return templates.TemplateResponse(
        request=request,
        name="app/recipe_detail.html",
        context={
            "user": current_user,
            "recipe": recipe
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
