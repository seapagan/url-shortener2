"""Main file for the API."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from rich import print

from config.helpers import get_api_version
from config.settings import get_settings
from database.db import database
from resources import config_error
from resources.routes import api_router

app = FastAPI(
    title=get_settings().api_title,
    description=get_settings().api_description,
    redoc_url=None,
    license_info=get_settings().license_info,
    contact=get_settings().contact,
    version=get_api_version(),
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)

app.include_router(api_router)
app.mount("/static", StaticFiles(directory="static"), name="static")

# set up CORS
cors_list = (get_settings().cors_origins).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Connect to the database on startup."""
    try:
        await database.connect()
    except Exception as exc:
        print(f"\n[red]ERROR: Have you set up your .env file?? ({exc})")
        print("[blue]Clearing routes and enabling error mesage.\n")
        app.routes.clear()
        app.include_router(config_error.router)


@app.on_event("shutdown")
async def shutdown():
    """Disconnect from the database on shutdown."""
    await database.disconnect()
