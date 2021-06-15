"""
CRUD common function used to access the data from db
"""

from sqlalchemy.orm import Session
from . import models, schemas

# TODO: Add more functions GET/POST and update schemas
# GET Functions
def get_pilot_by_name(db: Session, user_name: int):
    return db.query(models.Pilot).filter(models.Pilot.name == user_name).first()


def get_flight_by_date(db: Session, flight_date: str):
    return db.query(models.Flight).filter(models.Flight.flight_dt == flight_date).all()


def get_flight_by_year(db: Session, flight_year: int):
    return db.query(models.Flight).filter(models.Flight.flight_yr == flight_year).all()


def get_aircraft_by_tail(db: Session, tail_numb: str):
    return db.query(models.Aircraft).filter(models.Aircraft.tail_num == tail_numb).all()


# CREATE Functions
def create_flight(db: Session, flight: schemas.FlightCreate, pilot_id: int, aircraft_id: int):
    db_flight = models.Flight(**flight.dict(), pilot=pilot_id, aircraft=aircraft_id)
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def create_aircraft(db: Session, aircraft: schemas.AircraftCreate):
    pass


def create_pilot(db: Session, pilot: schemas.PilotCreate, pilot_name: str):
    db_pilot = models.Pilot(**pilot.dict(), name=pilot_name)
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot
