from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import models
from app.schema.pilotSchema import PilotCreate
from app.schema.hash import Hash


# Make Pilot-User with login creds
def create_pilot_user(db: Session, pilot: PilotCreate):
    hashedpwd = Hash.bcrypt(pilot.password)
    pilot_user = models.Pilot(password=hashedpwd,
                              name=pilot.name,
                              email=pilot.email)
    db.add(pilot_user)
    db.commit()
    db.refresh(pilot_user)
    return pilot_user


def get_pilot_by_id(db: Session, pilot_id: str):
    query = db.query(models.Pilot).filter(models.Pilot.id == pilot_id).first()
    if query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pilot with id {pilot_id} not found")
    return query


def get_pilot_by_email(db: Session,
                       pilot_email: str,
                       verify_only: bool = False):
    query = db.query(models.Pilot).filter(models.Pilot.email == pilot_email).first()
    if verify_only is True:
        return query
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Pilot with email {pilot_email} not found")
    return query
