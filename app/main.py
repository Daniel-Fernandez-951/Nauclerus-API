import uvicorn

import pandas as pd
from io import StringIO
from typing import Callable
from sqlalchemy.orm import Session
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI, APIRouter, Depends, HTTPException, File, UploadFile

from sqlUtils import models, crud
from sqlUtils.database import SessionLocal, engine
from sqlUtils.schemas.pilotSchema import Pilot, PilotCreate
from sqlUtils.schemas.flightSchema import Flight, FlightCreate
from sqlUtils.schemas.aircraftSchema import Aircraft, AircraftCreate
from sqlUtils.schemas.logbookSchema import LogbookCreate, Logbook


class UploadRoute(APIRoute):
    def __init__(self, path: str, endpoint: Callable, **kwargs):
        kwargs["include_in_schema"] = True
        super().__init__(path, endpoint, **kwargs)

        
app_up = APIRouter(route_class=UploadRoute)

# OpenAPI and Doc settings
API_VERSION = "0.0.5"
TAGS_METADATA = [
    {"name": "Pilot", "description": "Pilot POST and GET endpoints"},
    {"name": "Aircraft", "description": "Aircraft POST and GET endpoints"},
    {"name": "Logbook", "description": "Logbook POST and GET endpoints"},
    {"name": "Flight", "description": "Flight POST and GET endpoints"},
    {"name": "Upload", "description": "Upload logbook file"}
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
models.Base.metadata.create_all(bind=engine)
app = FastAPI(openapi_tags=TAGS_METADATA)
app.mount("/images", StaticFiles(directory="images"), name="images")
app.openapi = custom_openapi


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Endpoints
@app.get("/pilot/{pilot_id}",
         response_model=Pilot,
         summary="Get all Pilot data from pilot ID",
         tags=["Pilot"])
def g_pilot(pilot_id: int, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    if db_pilot is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")
    return db_pilot


@app.post("/pilot/new/",
          response_model=Pilot,
          summary="Make a new Pilot user",
          tags=["Pilot"])
def p_pilot(pilot: PilotCreate, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_name(db, pilot_name=pilot.name)
    if db_pilot:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_pilot(db=db, pilot=pilot)


@app.get("/logbook/all/{pilot_id}",
         summary="Get all logbook maps uploaded by pilot",
         tags=["Logbook"])
def g_logbook(pilot_id: int = None, db: Session = Depends(get_db)):
    if pilot_id is None:
        raise HTTPException(status_code=400, detail="Pilot ID needed")
    return crud.get_logbook_by_pilot(db=db, pilot_id=pilot_id)


@app.post("/logbook/",
          summary="Define Logbook layout to match uploaded fields to database",
          tags=["Logbook"])
def p_logbook(logbook: LogbookCreate, db: Session = Depends(get_db)):
    return crud.create_logbook(db=db, logbook=logbook)


@app.delete("/logbook/rm",
            summary="Remove pilot's uploaded logbook map",
            tags=["Logbook"])
def del_logbook(pilot_id: int, logbook_id: int, db: Session = Depends(get_db)):
    return crud.delete_logbook_map(db=db, pilot_id=pilot_id, logbook_id=logbook_id)


@app.get("/aircraft/s/tn/{ac_tail}",
         response_model=Aircraft,
         summary="Search aircraft by tail number",
         tags=["Aircraft"])
def search_tn(ac_tail: str = None, db: Session = Depends(get_db)):
    if ac_tail is None:
        raise HTTPException(status_code=400, detail="Missing Tail Number")
    return crud.get_aircraft_by_tail(db=db, tail_numb=ac_tail.upper())


@app.post("/aircraft/new/{pilot_id}",
          response_model=Aircraft,
          summary="Create new Aircraft linked to Pilot",
          tags=["Aircraft"])
def p_aircraft(pilot_id: int, aircraft: AircraftCreate, db: Session = Depends(get_db)):
    return crud.create_aircraft(db=db, aircraft=aircraft, pilot_id=pilot_id)


@app.post("/flight/", response_model=Flight, summary="Create a new Flight", tags=["Flight"])
def p_flight(flight: FlightCreate,
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


@app_up.post("/upload/{pilot_id}",
             summary="Upload Logbook data from outside source",
             tags=["Upload"])
def upload_logbook_file(file: UploadFile = File(...),
                        pilot_id: int = None,
                        db: Session = Depends(get_db)):
    if pilot_id is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")

    file_raw = file.file.read()
    file_pd = pd.read_csv(StringIO(str(file_raw, 'utf-8-sig')),
                          encoding='utf-8-sig',
                          parse_dates=['Date'],
                          ).fillna(0)
    print(file_pd["Aircraft"].describe())


app.include_router(app_up)

# Debugging portion
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, debug=True, reload=True)
