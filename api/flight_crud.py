from sqlalchemy.orm import Session

from models import models
from schema.flightSchema import FlightCreate


def get_flight_by_date(db: Session, flight_date: str):
    return db.query(models.Flight).filter(models.Flight.flight_dt == flight_date).all()


def get_flight_by_year(db: Session, flight_year: int):
    return db.query(models.Flight).filter(models.Flight.flight_yr == flight_year).all()


def create_flight(db: Session, flight: FlightCreate, pilot_id: str, aircraft_id: str):
    db_flight = models.Flight(**flight.dict())
    db_flight.pilot_id = pilot_id
    db_flight.aircraft_id = aircraft_id
    db.add(db_flight)
    db.commit()
    db.refresh(db_flight)
    return db_flight
