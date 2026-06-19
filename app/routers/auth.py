from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse

from app.database.database import get_db
from app.models.user import User
from app.services.recipe_service import get_recipes_by_user

from app.services.user_service import (create_user, get_user_by_email, authenticate_user)
from app.auth.jwt import create_access_token
from app.auth.dependencies import get_current_user

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

    response = RedirectResponse(url="/dashboard", status_code=303)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax"
    )

    return response


@router.get("/dashboard")
def dashboard(request: Request, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):

    recipes = get_recipes_by_user(db=db, user_id=current_user.id)

    return templates.TemplateResponse(
        request=request,
        name="app/dashboard.html",
        context={
            "user": current_user,
            "recipes": recipes
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
