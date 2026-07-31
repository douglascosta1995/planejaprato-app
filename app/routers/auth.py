from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.config import ADMIN_TOKEN
from app.database.database import get_db
from app.models import Recipe, MealPlan, ShoppingList
from app.models.user import User
from app.services.meal_plan_service import get_user_latest_meal_plan
from app.services.recipe_service import get_recipes_by_user, get_system_recipes, count_user_recipes, \
    count_system_recipes

from app.services.user_service import (create_user, get_user_by_email, authenticate_user)
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user
from app.utils.messages import MESSAGES

router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


@router.post("/register")
def register(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    name = name.strip()
    email = email.strip().lower()

    existing_user = get_user_by_email(db, email)

    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={
                "error": "Este e-mail já está cadastrado."
            }
        )

    try:
        create_user(db, name, email, password)

    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="auth/register.html",
            context={
                "error": "Ocorreu um erro ao criar sua conta. Tente novamente.",
                "name": name,
                "email": email
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="auth/register_success.html",
        context={}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/register.html",
        context={}
    )


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    email = email.strip().lower()
    user = authenticate_user(db, email, password)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="auth/home.html",
            context={
                "app_name": "PlanejaPrato",
                "error": "E-mail ou senha inválidos."
            }
        )

    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )

    user.last_login_at = datetime.utcnow()
    db.commit()

    response = RedirectResponse(url="/dashboard?message=login_success", status_code=303)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return response


@router.get("/dashboard")
def dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    recipes_user = get_recipes_by_user(db=db, user_id=current_user.id)[:4]
    recipes_system = get_system_recipes(db=db)[:4]

    total_user_recipes = count_user_recipes(db, current_user.id)
    total_system_recipes = count_system_recipes(db)

    message_key = request.query_params.get("message")

    message = MESSAGES.get(message_key)

    latest_meal_plan = get_user_latest_meal_plan(db=db, user_id=current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="app/dashboard.html",
        context={
            "user": current_user,
            "recipes_user": recipes_user,
            "recipes_system": recipes_system,
            "message": message,
            "latest_meal_plan": latest_meal_plan,
            "total_user_recipes": total_user_recipes,
            "total_system_recipes": total_system_recipes,
        }
    )


@router.get("/logout")
def logout():

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.delete_cookie(key="access_token")

    return response


@router.get("/demo", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="auth/demo_page.html",
        context={}
    )


@router.get("/guide")
def guide(request: Request, current_user: User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request=request,
        name="app/guide.html",
        context={
            "user": current_user
        }
    )


@router.get("/admin/{token}")
def admin_dashboard(token: str, request: Request, db: Session = Depends(get_db)):

    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=404)

    total_users = db.query(User).count()
    total_recipes = db.query(Recipe).count()
    total_meal_plans = db.query(MealPlan).count()
    total_shopping_lists = db.query(ShoppingList).count()

    last_users = (
        db.query(
            User,
            func.count(func.distinct(Recipe.id)).label("recipe_count"),
            func.count(func.distinct(MealPlan.id)).label("meal_plan_count")
        )
        .outerjoin(Recipe, Recipe.user_id == User.id)
        .outerjoin(MealPlan, MealPlan.user_id == User.id)
        .group_by(User.id)
        .order_by(User.id.desc())
        .limit(10)
        .all()
    )

    return templates.TemplateResponse(
        request=request,
        name="app/admin_dashboard.html",
        context={
            "user": "Admin",
            "total_users": total_users,
            "total_recipes": total_recipes,
            "total_meal_plans": total_meal_plans,
            "total_shopping_lists": total_shopping_lists,
            "last_users": last_users
        }
    )
