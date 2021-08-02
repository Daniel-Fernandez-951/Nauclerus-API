import uvicorn

import pandas as pd
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, APIRouter, Depends, HTTPException, File, UploadFile, Body
from fastapi.routing import APIRoute
from typing import Callable
from io import StringIO

from starlette.staticfiles import StaticFiles

from sqlUtils.schemas.pilotSchema import Pilot, PilotCreate
from sqlUtils.schemas.aircraftSchema import Aircraft, AircraftCreate
from sqlUtils.schemas.logbookSchema import LogbookCreate
from sqlUtils.schemas.flightSchema import Flight, FlightCreate
app = FastAPI()


class UploadRoute(APIRoute):
    def __init__(self, path: str, endpoint: Callable, **kwargs):
        kwargs["include_in_schema"] = False
        super().__init__(path, endpoint, **kwargs)


app_up = APIRouter(route_class=UploadRoute)


# Import local packages
from sqlUtils import models, crud
from sqlUtils.database import SessionLocal, engine


# OpenAPI and Doc settings
API_VERSION = "0.0.2"
tags_metadata = [
    {"name": "Universal", "description": "Works with all formats"},
    {"name": "Get GA", "description": "**ASA-SP-40** format"},
    {"name": "Post GA", "description": "**ASA-SP-40** format"}
]


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
        "url": "/images/logo2-nauclerusAPIV1_dark.png"
    }
    openapi_schema["license"] = {
        "name": "GPL-3.0",
        "url": "/app/LICENSE"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Instantiate
# TODO: Test pulling BASE from `from sqlUtils.database import Base`
models.Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=tags_metadata)
app.mount("/images", StaticFiles(directory="images"), name="images")
app.openapi = custom_openapi


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pilot/{pilot_id}", response_model=Pilot, tags=["Universal"])
def get_pilot(pilot_id: int, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    if db_pilot is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")
    return db_pilot


@app.post("/pilot/", response_model=Pilot, tags=["Universal"])
def create_pilot(pilot: PilotCreate, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_name(db, pilot_name=pilot.name)
    if db_pilot:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_pilot(db=db, pilot=pilot)


@app.post("/logbook/", tags=["Universal"])
def create_logbook(logbook: LogbookCreate, db: Session = Depends(get_db)):
    return crud.create_logbook(db=db, logbook=logbook)
                                                

@app.post("/aircraft/{pilot_id}", response_model=Aircraft, tags=["Post GA"])
def create_aircraft(pilot_id: int, aircraft: AircraftCreate, db: Session = Depends(get_db)):
    return crud.create_aircraft(db=db, aircraft=aircraft, pilot_id=pilot_id)


@app.post("/flight/", response_model=Flight, tags=["Post GA"])
def create_flight(flight: FlightCreate,
                  pilot_id: int = None,
                  aircraft_id: int = None,
                  db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    db_ac = crud.get_aircraft_by_id(db, ac_id=aircraft_id)
    if db_pilot is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")
    if db_ac is None:
        raise HTTPException(status_code=422, detail="Aircraft ID required.")
    return crud.create_flight(db=db, flight=flight, pilot_id=pilot_id, aircraft_id=aircraft_id)


@app_up.post("/upload/ASA-SP-40/")
def upload_file_asasp40(file: UploadFile = File(...),
                        pilot_id: int = None,
                        aircraft_id: int = None,
                        db: Session = Depends(get_db)):
    if pilot_id or aircraft_id is None:
        raise HTTPException(status_code=422, detail="Pilot and Aircraft ID are required.")

    file_raw = file.file.read()
    file_pd = pd.read_csv(StringIO(str(file_raw, 'utf-8-sig')),
                          encoding='utf-8-sig',
                          parse_dates=['Date'],
                          ).fillna(0)
    print(file_pd.columns)


app.include_router(app_up)


# Debugging portion
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, debug=True, reload=True)