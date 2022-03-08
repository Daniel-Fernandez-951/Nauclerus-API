from fastapi import APIRouter, Depends

from app.database import configuration
from app.schema.oa2 import get_current_user


router = APIRouter(tags=["Logbook"],
                   prefix="/logbook",
                   dependencies=[Depends(get_current_user)])
get_db = configuration.get_db
