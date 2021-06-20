"""
Pydantic Models: Define a valid data shape (schema).
"""

from typing import Optional, List
from pydantic import BaseModel
from datetime import date


# Pilot
class PilotBase(BaseModel): # Base model lists common between reading/creating
    name: str


class PilotCreate(PilotBase): # Create model only lists what to change
    pass # Inherit from PilotBase


# Aircraft
class AircraftBase(BaseModel):
    tail_num: str


class AircraftCreate(AircraftBase):
    pass


# Flight
class FlightBase(BaseModel):
    flight_dt: date
    flight_yr: int
    dest_t: str
    dest_f: str
    notes: Optional[str] = None
    ifr_app: Optional[int] = 0
    landings: int = 1
    sel_t: float
    mel_t: Optional[float] = 0.0
    cross_c: Optional[float] = 0.0
    day: Optional[float] = 0.0
    night: Optional[float] = 0.0
    actual_inst: Optional[float] = 0.0
    sim_inst: Optional[float] = 0.0
    ground_train: Optional[float] = 0.0
    dual_rec: Optional[float] = 0.0
    pic: float
    ft_total: float


class FlightCreate(FlightBase):
    pass


# Reading and Returning Section
class Aircraft(AircraftBase):
    id: int
    pilot_id: int
    tail_num: str

    class Config:
        orm_mode = True


class Flight(FlightBase):
    pilot: int
    aircraft: int
    flight_dt: date
    flight_yr: int
    dest_t: str
    dest_f: str
    notes: str
    ifr_app: int
    landings: int
    sel_t: float
    mel_t: float
    cross_c: float
    day: float
    night: float
    actual_inst: float
    sim_inst: float
    ground_train: float
    dual_rec: float
    pic: float
    ft_total: float

    class Config:
        orm_mode = True


class Pilot(PilotBase): # Model for reading/returning
    id: int
    name: str
    rec_flights: List[Flight] = []
    piloted_ac: List[Aircraft] = []

    class Config:
        orm_mode = True
