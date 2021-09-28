"""
CRUD common function used to access the data from db
"""
import json

from sqlalchemy.orm import Session
from json import encoder
from . import models
from .schemas.pilotSchema import PilotCreate
from .schemas.aircraftSchema import AircraftCreate
from .schemas.flightSchema import FlightCreate
from .schemas.logbookSchema import LogbookCreate, LogbookMap, Logbook


# TODO: Add more functions GET/POST and update schemas
# GET Functions
def get_pilot_by_name(db: Session, pilot_name: str):
    return db.query(models.Pilot).filter(models.Pilot.name == pilot_name).first()


def get_pilot_by_id(db: Session, pilot_id: int):
    return db.query(models.Pilot).filter(models.Pilot.id == pilot_id).first()


def get_flight_by_date(db: Session, flight_date: str):
    return db.query(models.Flight).filter(models.Flight.flight_dt == flight_date).all()


def get_flight_by_year(db: Session, flight_year: int):
    return db.query(models.Flight).filter(models.Flight.flight_yr == flight_year).all()


def get_logbook_by_pilot(db: Session, pilot_id: int):
    return db.query(models.Logbook).filter(models.Logbook.pilot_id == pilot_id).all()


def get_aircraft_by_tail(db: Session, tail_numb: str):
    return db.query(models.Aircraft).filter(models.Aircraft.ac_tail == tail_numb).first()


def get_aircraft_by_id(db: Session, ac_id: int):
    return db.query(models.Aircraft).filter(models.Aircraft.id == ac_id).first()


# CREATE Functions
def create_flight(db: Session, flight: FlightCreate, pilot_id: int, aircraft_id: int):
    db_flight = models.Flight(**flight.dict())
    db_flight.pilot_id = pilot_id
    db_flight.aircraft_id = aircraft_id
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight


def create_aircraft(db: Session, aircraft: AircraftCreate, pilot_id: int):
    db_aircraft = models.Aircraft(**aircraft.dict(), pilot_id=pilot_id)
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft


def create_pilot(db: Session, pilot: PilotCreate):
    db_pilot = models.Pilot(**pilot.dict())
    db.add(db_pilot)
    db.commit()
    db.refresh(db_pilot)
    return db_pilot


def create_logbook(db: Session, logbook: LogbookCreate):
    # TODO: This may be wrong, need to format HEADER_TITLES to string with schema
    db_logbook = models.Logbook(**logbook.dict())
    db.add(db_logbook)
    db.commit()
    db.refresh(db_logbook)
    return db_logbook


# DELETE Functions
def delete_logbook_map(db: Session, pilot_id: int, logbook_id: int):
    rm_logbook = db.query(models.Logbook)\
        .filter(models.Logbook.id == logbook_id,
                models.Logbook.pilot_id == pilot_id)\
        .first()
    db.delete(rm_logbook)
    db.commit()
    return rm_logbook
