from sqlalchemy.orm import Session

from app.models import models
from app.schema.aircraftSchema import AircraftCreate


def get_aircraft_by_tail(db: Session, tail_numb: str):
    return db.query(models.Aircraft).filter(models.Aircraft.ac_tail == tail_numb).first()


def get_aircraft_by_id(db: Session, ac_id: str):
    return db.query(models.Aircraft).filter(models.Aircraft.id == ac_id).first()


def create_aircraft(db: Session, aircraft: AircraftCreate, pilot_id: str):
    db_aircraft = models.Aircraft(**aircraft.dict(), pilot_id=pilot_id)
    db.add(db_aircraft)
    db.commit()
    db.refresh(db_aircraft)
    return db_aircraft
