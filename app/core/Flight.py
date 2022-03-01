from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from app.api import logbook_crud
from app.database import configuration
from app.schema.oa2 import get_current_user
from app.schema.pilotSchema import PilotSecure
from app.schema.logbookSchema import Logbook, LogbookCreate


router = APIRouter(tags=["Logbook"],
                   prefix="/logbook",
                   dependencies=[Depends(get_current_user)])
get_db = configuration.get_db
