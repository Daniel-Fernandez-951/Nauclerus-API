from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.configuration import get_db
from app.schema import pilotSchema
from app.models import models
from app.schema.hash import Hash
from app.schema.token import create_access_token

router = APIRouter(prefix="/login", tags=["Authentication"],
                   include_in_schema=False)


@router.post("/")
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    pilot: pilotSchema.PilotSecure = db.query(models.Pilot)\
        .filter(models.Pilot.email == request.username)\
        .first()
    if not pilot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Login Failure: Email/Password")

    if not Hash.verify(pilot.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Login Failure: Email/Password")
    
    access_token = create_access_token(
        data={"sub": pilot.email,
              "originTime": str(pilot.created_at),
              "id": str(pilot.id)
              }
    )
    return {"access_token": access_token,
            "token_type": "bearer"}
