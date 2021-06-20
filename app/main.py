"""
File upload: https://stackoverflow.com/questions/64232908/how-to-add-multiple-body-params-with-fileupload-in-fastapi
"""

from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, UploadFile

# Import local packages
from sqlUtils import models, crud, schemas
from sqlUtils.database import SessionLocal, engine

# Instantiate
models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/pilot/{pilot_id}", response_model=schemas.Pilot)
def get_pilot(pilot_id: int, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    return db_pilot


@app.post("/pilot/", response_model=schemas.Pilot)
def create_pilot(pilot: schemas.PilotCreate, db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_name(db, pilot_name=pilot.name)
    if db_pilot:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_pilot(db=db, pilot=pilot)


@app.post("/aircraft/{pilot_id}", response_model=schemas.Aircraft)
def create_aircraft(pilot_id: int, aircraft: schemas.AircraftCreate, db: Session = Depends(get_db)):
    return crud.create_aircraft(db=db, aircraft=aircraft, pilot_id=pilot_id)


@app.post("/flight/", response_model=schemas.Flight)
def create_flight(flight: schemas.FlightCreate,
                  pilot_id: int = None,
                  aircraft_id: int = None,
                  db: Session = Depends(get_db)):
    db_pilot = crud.get_pilot_by_id(db, pilot_id=pilot_id)
    db_ac = crud.get_aircraft_by_id(db, ac_id=aircraft_id)
    if db_pilot is None:
        raise HTTPException(status_code=404, detail="Pilot ID not found")
    if db_ac is None:
        raise HTTPException(status_code=404, detail="Aircraft ID not found")
    return crud.create_flight(db=db, flight=flight, pilot_id=pilot_id, aircraft_id=aircraft_id)
