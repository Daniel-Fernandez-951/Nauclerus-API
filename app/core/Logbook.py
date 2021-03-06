from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api import logbook_crud
from app.database import configuration
from app.schema.logbookSchema import Logbook, LogbookCreate
from app.schema.oa2 import get_current_user
from app.schema.tokenSchema import TokenData

router = APIRouter(tags=["Logbook"],
                   prefix="/logbook",
                   dependencies=[Depends(get_current_user)])
get_db = configuration.get_db


@router.get("/pilot",
            response_model=Optional[List[Logbook]],
            summary="Get all logbook maps uploaded by pilot",
            status_code=status.HTTP_200_OK)
def get_logbook(db: Session = Depends(get_db),
                token_data: TokenData = Depends(get_current_user)):
    return logbook_crud.get_logbook_by_pilot(db=db,
                                             pilot_id=token_data.pilot_id)


@router.post("/new",
             summary="Get all logbook maps uploaded by pilot",
             status_code=status.HTTP_201_CREATED)
def post_logbook(logbook: LogbookCreate,
                 db: Session = Depends(get_db),
                 token_data: TokenData = Depends(get_current_user)):
    return logbook_crud.create_logbook(db=db,
                                       logbook=logbook,
                                       pilot_id=token_data.pilot_id)


# @router.delete("/rm",
#                summary="Remove pilot's uploaded logbook map",
#                status_code=status.HTTP_202_ACCEPTED)
