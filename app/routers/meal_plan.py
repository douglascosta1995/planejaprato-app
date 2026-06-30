from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from app.services.meal_plan_service import (
    generate_meal_plan,
    get_meal_plan_by_id,
    organize_meal_plan,
    generate_shopping_list,
    delete_meal_plan
)

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get("/meal-plans/new")
def new_meal_plan(request: Request, current_user: User = Depends(get_current_user)):

    return templates.TemplateResponse(
        request=request,
        name="app/new_meal_plan.html",
        context={
            "user": current_user
        }
    )


@router.post("/meal-plans")
def create_meal_plan(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    meal_plan = generate_meal_plan(
        db=db,
        user_id=current_user.id
    )

    if meal_plan is None:
        return templates.TemplateResponse(
            request=request,
            name="app/new_meal_plan.html",
            context={
                "user": current_user,
                "error": "Não foi possível gerar o cardápio. Cadastre pelo menos uma receita para cada categoria."
            }
        )

    return RedirectResponse(
        url=f"/meal-plans/{meal_plan.id}?message=meal_plan_created",
        status_code=303
    )


@router.get("/meal-plans/{meal_plan_id}")
def meal_plan_detail(meal_plan_id: int, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    meal_plan = get_meal_plan_by_id(
        db,
        meal_plan_id
    )

    days = organize_meal_plan(meal_plan)

    if not meal_plan:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    if meal_plan.user_id != current_user.id:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    return templates.TemplateResponse(
        request=request,
        name="app/meal_plan_detail.html",
        context={
            "user": current_user,
            "meal_plan": meal_plan,
            "days": days
        }
    )


@router.post("/meal-plans/{meal_plan_id}/delete")
def delete_meal_plan_route(
    meal_plan_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    meal_plan = get_meal_plan_by_id(
        db,
        meal_plan_id
    )

    if not meal_plan:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    if meal_plan.user_id != current_user.id:
        return RedirectResponse(
            "/dashboard",
            status_code=303
        )

    delete_meal_plan(
        db=db,
        meal_plan=meal_plan
    )

    return RedirectResponse(
        "/dashboard?message=meal_plan_deleted",
        status_code=303
    )


@router.get("/meal-plans/{meal_plan_id}/shopping-list")
def shopping_list(meal_plan_id: int, request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    meal_plan = get_meal_plan_by_id(db, meal_plan_id)

    if not meal_plan or meal_plan.user_id != current_user.id:
        return RedirectResponse("/dashboard", status_code=303)

    shopping_list = generate_shopping_list(meal_plan)

    return templates.TemplateResponse(
        request=request,
        name="app/shopping_list.html",
        context={
            "user": current_user,
            "meal_plan": meal_plan,
            "shopping_list": shopping_list
        }
    )
