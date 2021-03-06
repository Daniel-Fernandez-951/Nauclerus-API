from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import pilot_crud
from app.database import configuration
from app.schema.oa2 import get_current_user
from app.schema.pilotSchema import Pilot, PilotCreate
from app.schema.tokenSchema import TokenData

router = APIRouter(tags=["Pilot"], prefix="/pilot")
get_db = configuration.get_db


@router.get("/id",
            response_model=Pilot,
            summary="Get all Pilot data by pilot ID",
            status_code=status.HTTP_200_OK)
def g_pilot(db: Session = Depends(get_db),
            token_data: TokenData = Depends(get_current_user)):
    db_pilot = pilot_crud.get_pilot_by_id(db, pilot_id=token_data.pilot_id)
    if db_pilot is None:
        raise HTTPException(status_code=422, detail="Pilot ID required.")
    return db_pilot


@router.get("/email",
            response_model=Pilot,
            summary="Get all Pilot data by email",
            status_code=status.HTTP_200_OK)
def g_pilot_email(db: Session = Depends(get_db),
                  token_data: TokenData = Depends(get_current_user)):
    db_pilot = pilot_crud.get_pilot_by_email(db, pilot_email=token_data.email)
    if not db_pilot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Name not found")
    return db_pilot


@router.post("/new",
             response_model=Pilot,
             summary="Make a new Pilot user (required for login)",
             status_code=status.HTTP_201_CREATED)
def p_pilot(pilot: PilotCreate, db: Session = Depends(get_db)):
    db_pilot = pilot_crud.get_pilot_by_email(db,
                                             pilot_email=pilot.email,
                                             verify_only=True)
    if db_pilot:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Email already registered")
    return pilot_crud.create_pilot_user(db=db, pilot=pilot)
