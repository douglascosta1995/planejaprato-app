from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routers.auth import router as auth_router
from app.routers.recipes import router as recipe_router
from app.routers.ingredient import router as ingredient_router
from app.routers.meal_plan import router as meal_plan_router
from app.routers.sitemap import router as sitemap_router

from app.database.database import Base
from app.database.database import engine
from app.database.database import SessionLocal

from app.scripts.initialize_db import initialize_database

import app.models

app = FastAPI()

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    initialize_database(db)
finally:
    db.close()

app.include_router(auth_router)
app.include_router(recipe_router)
app.include_router(ingredient_router)
app.include_router(meal_plan_router)
app.include_router(sitemap_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(
    directory="app/templates"
)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
):
    if exc.status_code == 401:
        response = RedirectResponse(
            url="/",
            status_code=303
        )

        response.delete_cookie("access_token")

        return response

    if exc.status_code == 404:
        return RedirectResponse(
            url="/404",
            status_code=303
        )

    return exc

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
):
    return RedirectResponse(
        url="/404",
        status_code=303
    )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="auth/home.html",
        context={
            "app_name": "PlanejaPrato"
        }
    )


@app.get("/404", response_class=HTMLResponse)
def not_found(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="errors/404.html"
    )
