from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.routing import APIRoute
from sqlalchemy.orm import Session
from typing import Callable
import pandas as pd
from io import StringIO

from database import configuration
from schema.oa2 import get_current_user
from schema.tokenSchema import TokenData


get_db = configuration.get_db


class UploadRoute(APIRoute):
    def __init__(self, path: str,
                 endpoint: Callable,
                 **kwargs):
        kwargs["include_in_schema"] = True
        super().__init__(path, endpoint, **kwargs)


router = APIRouter(route_class=UploadRoute,
                   tags=["Upload"],
                   prefix="/upload")


# TODO: Fully implement to database
@router.post("/",
             summary="Upload Logbook data from CSV file",
             status_code=status.HTTP_201_CREATED)
def upload_logbook_file(file: UploadFile = File(...),
                        db: Session = Depends(get_db),
                        token_data: TokenData = Depends(get_current_user)):
    if token_data.pilot_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pilot ID required.")

    file_raw = file.file.read()
    file_pd = pd.read_csv(StringIO(str(file_raw, 'utf-8-sig')),
                          encoding='utf-8-sig',
                          parse_dates=['Date'],
                          ).fillna(0)
    print(file_pd["Aircraft"].describe())
