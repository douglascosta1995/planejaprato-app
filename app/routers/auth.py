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

from app.services.user_service import (create_user, get_user_by_email, authenticate_user)

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
            name="register.html",
            context={
                "error": "Este e-mail já está cadastrado."
            }
        )

    try:
        create_user(db, name, email, password)

    except Exception:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "error": "Ocorreu um erro ao criar sua conta. Tente novamente.",
                "name": name,
                "email": email
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="register_success.html",
        context={}
    )


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    email = email.strip().lower()
    user = authenticate_user(db, email, password)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="home.html",
            context={
                "app_name": "PlanejaPrato",
                "error": "E-mail ou senha inválidos."
            }
        )

    return RedirectResponse(
        url="/dashboard",
        status_code=303
    )


@router.get("/dashboard")
def dashboard():

    return {
        "message": "Bem-vindo ao PlanejaPrato"
    }
