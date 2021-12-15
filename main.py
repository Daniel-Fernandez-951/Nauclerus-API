from fastapi import FastAPI
from starlette.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
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
def index():
    return """
    <!doctype html> <!-- Important: must specify -->
<html>
  <head>
    <meta charset="utf-8"> <!-- Important: rapi-doc uses utf8 characters -->
    <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
  </head>
  <body>
    <rapi-doc 
      spec-url = "openapi.json"
      theme = "dark"
      schema-style = "table"
      render-style = "view"
      allow-spec-url-load = "false"
      allow-spec-file-load = "false"
      >
    <img slot="logo" src="/static/logo2-nauclerusAPIV1_dark.png" style="width:200px; height:75px"/>
    </rapi-doc>
  </body>
</html>
    """
# """
    # <!Doctype html>
    # <html>
    #     <body>
    #         <h1>Nauclerus API</h1>
    #         <div class="btn-group">
    #             <a href="/docs"><button>SwaggerUI</button></a>
    #             <a href="/redoc"><button>Redoc</button></a>
    #         </div>
    #     </body>
    # </html>
    # """
