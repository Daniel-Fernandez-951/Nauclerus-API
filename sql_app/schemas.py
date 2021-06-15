"""
Pydantic Models: Define a valid data shape (schema).
"""

from typing import Optional
from pydantic import BaseModel
from datetime import date


# Pilot
class PilotBase(BaseModel):
    name: str


class PilotCreate(PilotBase):
    pass


class Pilot(PilotBase):
    id: int

    class Config:
        orm_mode = True


# Aircraft
class AircraftBase(BaseModel):
    tail_num: str


class AircraftCreate(AircraftBase):
    pass


class Aircraft(AircraftBase):
    id: int
    pilot_id: int

    class Config:
        orm_mode = True


# Flight
class FlightBase(BaseModel):
    flight_dt: date
    flight_yr: int
    dest_t: str
    dest_f: str
    notes: Optional[str] = None
    ifr_app: Optional[int] = 0
    landings: int
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
    pilot: int
    aircraft: int


class Flight(FlightBase):
    id: int
    pilot: int
    aircraft: int

    class Config:
        orm_mode = True
