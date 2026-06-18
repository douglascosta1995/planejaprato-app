from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from app.routers.auth import router as auth_router

from app.database.database import Base
from app.database.database import engine

from app.models.user import User
from app.models.ingredient import Ingredient
from app.models.recipe import Recipe

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
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
