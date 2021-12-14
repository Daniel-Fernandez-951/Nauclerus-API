from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from schema.oa2 import get_current_user
from database import configuration
from schema.pilotSchema import Pilot, PilotCreate, PilotSecure
from schema.tokenSchema import TokenData
from api import pilot_crud

router = APIRouter(tags=["Pilot"], prefix="/pilot")
get_db = configuration.get_db


@router.get("/id/{pilot_id}",
            response_model=Pilot,
            summary="Get all Pilot data by pilot ID",
            status_code=status.HTTP_200_OK)
def g_pilot(pilot_id: str,
            db: Session = Depends(get_db)):
    db_pilot = pilot_crud.get_pilot_by_id(db, pilot_id=pilot_id)
    if db_pilot is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")
    return db_pilot


@router.get("/email",
            response_model=Pilot,
            summary="Get all Pilot data by email",
            status_code=status.HTTP_200_OK)
def g_pilot_name(db: Session = Depends(get_db),
                 token_data: TokenData = Depends(get_current_user)):
    db_pilot = pilot_crud.get_pilot_by_email(db, pilot_email=token_data.email)
    if not db_pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Name not found")
    return db_pilot


@router.post("/new",
             response_model=Pilot,
             summary="Make a new Pilot user (required for login)",
             status_code=status.HTTP_201_CREATED)
def p_pilot(pilot: PilotCreate, db: Session = Depends(get_db)):
    # db_pilot = pilot_crud.get_pilot_by_email(db, pilot_email=pilot.email)
    # if db_pilot:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT,
    #                         detail="Name already registered")
    return pilot_crud.create_pilot_user(db=db, pilot=pilot)
