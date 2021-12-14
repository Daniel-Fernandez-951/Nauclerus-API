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
