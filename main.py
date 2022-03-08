import sys
import traceback

import uvicorn
from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# API Metrics--MOESIF
from moesifasgi import MoesifMiddleware
from starlette.responses import HTMLResponse

# Import Run config
import app.config.run_config as cfg
from app.config.open_api import API_VERSION, MOESIF_SETTINGS, TAGS_METADATA
# Import router files
from app.core import Auth, Logbook, Pilot, Upload
from app.database.configuration import engine
# Import local files
from app.models import models


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


if __name__ == '__main__':
    print(f"Starting Nauclerus API --> {cfg.api['host']}:{cfg.api['port']}\n")

    try:
        uvicorn.run(
            "main:app",
            host=cfg.api['host'],
            port=cfg.api['port'],
            workers=int(cfg.api['workers']),
            log_level=cfg.api['log_level'],
            reload=bool(cfg.api['reload']),
            debug=bool(cfg.api['debug'])
        )
    except KeyboardInterrupt:
        print("Stopping Nauclerus API")
    except Exception as e:
        print(f"Start Failed\n{'#'*100}")
        traceback.print_exc(file=sys.stdout)
        print(e)
        print(f"Exiting\n{'#'*100}")
    print("\n\n")
