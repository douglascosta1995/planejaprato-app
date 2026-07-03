from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from app.routers.auth import router as auth_router
from app.routers.recipes import router as recipe_router
from app.routers.ingredient import router as ingredient_router
from app.routers.meal_plan import router as meal_plan_router

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
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(
    directory="app/templates"
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
