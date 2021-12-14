from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import models
from schema.logbookSchema import LogbookCreate


def get_logbook_by_pilot(db: Session, pilot_id: str):
    query = db.query(models.Logbook).filter(models.Logbook.pilot_id == pilot_id).all()
    if query == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Logbook with pilot-id of {pilot_id} not found")
    return query


def create_logbook(db: Session, logbook: LogbookCreate):
    # TODO: This may be wrong, need to format HEADER_TITLES to string with schema
    db_logbook = models.Logbook(**logbook.dict())
    db.add(db_logbook)
    db.commit()
    db.refresh(db_logbook)
    return db_logbook


def delete_logbook_map(db: Session, pilot_id: str, logbook_id: str):
    rm_logbook = db.query(models.Logbook)\
        .filter(models.Logbook.id == logbook_id,
                models.Logbook.pilot_id == pilot_id)\
        .first()
    if rm_logbook == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Logbook with id {logbook_id} and pilot-id {pilot_id} not found")
    db.delete(rm_logbook)
    db.commit()
    return rm_logbook
