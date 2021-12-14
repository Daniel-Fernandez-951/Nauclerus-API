from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from api import logbook_crud
from database import configuration
from schema.oa2 import get_current_user
from schema.pilotSchema import PilotSecure
from schema.logbookSchema import Logbook, LogbookCreate


router = APIRouter(tags=["Logbook"],
                   prefix="/logbook",
                   dependencies=[Depends(get_current_user)])
get_db = configuration.get_db


@router.get("/pilot/{pilot_id}",
            response_model=Logbook,
            summary="Get all logbook maps uploaded by pilot",
            status_code=status.HTTP_200_OK)
def get_logbook(pilot_id: str,
                db: Session = Depends(get_db),
                current_user: PilotSecure = Depends(get_current_user)):
    return logbook_crud.get_logbook_by_pilot(db=db, pilot_id=pilot_id)


@router.post("/pilot/{pilot_id}",
             response_model=Logbook,
             summary="Get all logbook maps uploaded by pilot",
             status_code=status.HTTP_201_CREATED)
def post_logbook(logbook: LogbookCreate, db: Session = Depends(get_db)):
    return logbook_crud.create_logbook(db=db, logbook=logbook)


# @router.delete("/rm",
#                summary="Remove pilot's uploaded logbook map",
#                status_code=status.HTTP_202_ACCEPTED)
