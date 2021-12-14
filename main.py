from fastapi import FastAPI
from starlette.responses import HTMLResponse
# Import local files
from models import models
from database.configuration import engine
# Import router files
from core import Auth, Aircraft, Flight, Logbook, Pilot

API_VERSION = "1.0"

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Nauclerus API",
    description="Logbook API for all Pilots",
    version=API_VERSION
)

app.include_router(Pilot.router)
# app.include_router(Aircraft.router)
app.include_router(Logbook.router)
# app.include_router(Flight.router)
app.include_router(Auth.router)


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
