from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
# Import local files
from models import models
from database.configuration import engine
# Import router files
from core import Auth, Aircraft, Flight, Logbook, Pilot, Upload
from config.open_api import TAGS_METADATA, API_VERSION, MOESIF_SETTINGS
# API Metrics--MOESIF
from moesifasgi import MoesifMiddleware


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Nauclerus Logbook API",
        version=API_VERSION,
        description="Aviation logbook API for all pilots.",
        routes=app.routes,
        tags=TAGS_METADATA
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/static/logo2-nauclerusAPIV1_dark.png"
    }
    openapi_schema["license"] = {
        "name": "GPL-3.0",
        "url": "/static/LICENSE"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Custom Docs
rapidoc = Jinja2Templates(directory="static")

models.Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=TAGS_METADATA)
app.openapi = custom_openapi
app.mount("/static", StaticFiles(directory="static"), name="static")

# API Monitoring
app.add_middleware(MoesifMiddleware, settings=MOESIF_SETTINGS)

app.include_router(Pilot.router)
# app.include_router(Aircraft.router)
app.include_router(Logbook.router)
# app.include_router(Flight.router)
app.include_router(Auth.router)
app.include_router(Upload.router)


@app.get("/",
         response_class=HTMLResponse,
         include_in_schema=False)
def index(request: Request):
    return rapidoc.TemplateResponse("html/rapidoc.html", {"request": request})
