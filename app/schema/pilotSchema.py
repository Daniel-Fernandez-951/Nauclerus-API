from pydantic import BaseModel, UUID4
from pydantic.networks import EmailStr
from typing import List, Optional
from datetime import datetime

from .flightSchema import Flight
from .aircraftSchema import Aircraft
from .logbookSchema import Logbook


# Base model lists common between reading/creating
class PilotBase(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]


# Create model only lists what to change
class PilotCreate(PilotBase):
    password: str


class PilotUpdate(PilotCreate):
    pass


# Arbitrary data upon creation
class PilotSecure(BaseModel):
    email: Optional[EmailStr]
    id: Optional[UUID4]
    password: str
    created_at: Optional[str] = datetime.utcnow()


# Model for reading/returning
class Pilot(PilotBase):
    id: UUID4
    rec_flights: List[Flight] = []
    piloted_ac: List[Aircraft] = []

    class Config:
        orm_mode = True