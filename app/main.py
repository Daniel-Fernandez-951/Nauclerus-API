"""
File upload: https://stackoverflow.com/questions/64232908/how-to-add-multiple-body-params-with-fileupload-in-fastapi
"""

from sqlalchemy.orm import Session
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI, Depends, HTTPException, UploadFile


# Import local packages
from sqlUtils import models, crud, schemas
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
    openapi_schema["servers"] = [{
        "url": "localhost",
        "description": "Development server"
    }]
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


@app.get("/pilot/{pilot_id}", response_model=schemas.Pilot, tags=["Universal"])
def get_pilot(pilot_id: int, db: Session = Depends(get_db)):
    """
    Pass ID of pilot to get Pilot object.

    - **pilot_id**: Unique ID of pilot when created

    _Response:_
    - **id**: Unique NUMBER representing Pilot
    - **name**: Unique STRING representing Pilot
    - **rec_flights**: LIST of flights recorded by Pilot or []
    - **piloted_ac**: LIST of aircrafts flown by Pilot or []
    """
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    if db_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot with ID does not exist")
    return db_pilot


@app.post("/pilot/", response_model=schemas.Pilot, tags=["Universal"])
def create_pilot(pilot: schemas.PilotCreate, db: Session = Depends(get_db)):
    """
    Create a Pilot with a unique name. Without a Pilot, new Aircraft and Flight are not possible.

    - **name**: Unique name of Pilot

    _Response:_
    - **id**: Unique NUMBER representing Pilot
    - **name**: Unique STRING representing Pilot
    - **rec_flights**: LIST of flights recorded by Pilot or []
    - **piloted_ac**: LIST of aircrafts flown by Pilot or []
    """
    db_pilot = crud.get_pilot_by_name(db, pilot_name=pilot.name)
    if db_pilot:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_pilot(db=db, pilot=pilot)


@app.post("/aircraft/{pilot_id}", response_model=schemas.Aircraft, tags=["Post GA"])
def create_aircraft(pilot_id: int, aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    """
    Create an Aircraft that is related to a Pilot. Pass Pilot ID in URL

    - **tail_num**: Unique STRING representing Aircraft tail number

    _Response:_
    - **id**: Unique NUMBER representing Aircraft ID
    - **pilot_id**: NUMBER representing Pilot
    - **tail_num**: Unique STRING representing aircraft tail number
    """
    return crud.create_aircraft(db=db, aircraft=aircraft, pilot_id=pilot_id)


@app.post("/flight/", response_model=schemas.Flight, tags=["Post GA"])
def create_flight(flight: schemas.FlightCreate,
                  pilot_id: int = None,
                  aircraft_id: int = None,
                  db: Session = Depends(get_db)):
    """
    Log a flight and link to a Pilot and Aircraft.


    _Input & Response_
    - **pilot_id**: Unique Pilot ID from an active Pilot
    - **aircraft_id**: Unique Aircraft ID from an active Aircraft
    - **flight_dt**: Flight DATE (YYYY-MM-DD)
    - **flight_yr**: Flight year (YYYY)
    - **dest_t**: Destination airport identifier STRING (KSFO)
    - **dest_f**: Departure airport identifier STRING (KSFO)
    - **notes**: Remarks and any notes about the flight STRING
    - **ifr_app**: NUMBER of IFR approaches (default = 0)
    - **landings**: NUMBER of landings (default = 1)
    - **sel_t**: Single Engine Land FLOAT time (default = 0)
    - **mel_t**: Multi-Engine Land FLOAT time (default = 0)
    - **cross_c**: Cross-Country FLOAT time (default = 0)
    - **day**: Day flight time FLOAT (default = 0)
    - **night**: Night flight time FLOAT (default = 0)
    - **actual_inst**: Actual Instrument FLOAT time (default = 0)
    - **sim_inst**: Simulated Instrument FLOAT time (default = 0)
    - **ground_train**: Ground Training FLOAT time (default = 0)
    - **dual_rec**: Dual Received FLOAT time (default = 0)
    - **pic**: Pilot In Command FLOAT time (default = 0)
    - **ft_total**: Total Flight FLOAT time (default = 0)
    """
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    db_ac = crud.get_aircraft_by_id(db, ac_id=aircraft_id)
    if db_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot ID not found")
    if db_ac is None:
        raise HTTPException(status_code=404, detail="Aircraft ID not found")
    return crud.create_flight(db=db, flight=flight, pilot_id=pilot_id, aircraft_id=aircraft_id)
