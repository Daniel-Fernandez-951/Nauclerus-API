from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
# Import local files
from models import models
from database.configuration import engine
# Import router files
from core import Auth, Aircraft, Flight, Logbook, Pilot, Upload
from config.open_api import TAGS_METADATA, API_VERSION


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Nauclerus Logbook API",
        version=API_VERSION,
        description="Aviation logbook API for all pilots.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "/"
    }
    openapi_schema["license"] = {
        "name": "GPL-3.0",
        "url": "/app/LICENSE"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


models.Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=TAGS_METADATA)
app.openapi = custom_openapi

app.include_router(Pilot.router)
# app.include_router(Aircraft.router)
app.include_router(Logbook.router)
# app.include_router(Flight.router)
app.include_router(Auth.router)
app.include_router(Upload.router)


@app.get("/",
         response_class=HTMLResponse,
         include_in_schema=False)
def index():
    return """
    <!Doctype html>
    <html>
        <body>
            <h1>Nauclerus API</h1>
            <div class="btn-group">
                <a href="/docs"><button>SwaggerUI</button></a>
                <a href="/redoc"><button>Redoc</button></a>
            </div>
        </body>
    </html>
    """
