from pydantic import BaseModel
from typing import List

from .flightSchema import Flight
from .aircraftSchema import Aircraft
from .logbookSchema import Logbook


# Base model lists common between reading/creating
class PilotBase(BaseModel):
    name: str


# Create model only lists what to change
class PilotCreate(PilotBase):
    pass


# Model for reading/returning
class Pilot(PilotBase):
    id: int
    rec_flights: List[Flight] = []
    piloted_ac: List[Aircraft] = []
    logbook: List[Logbook] = []

    class Config:
        orm_mode = True
