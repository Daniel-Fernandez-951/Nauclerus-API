from pydantic import BaseModel, UUID4
from datetime import date
from typing import Optional
from .aircraftSchema import Aircraft


class FlightBase(BaseModel):
    pilot_id: UUID4
    aircraft_id: UUID4
    year: int
    date: date
    fl_from: str
    fl_to: str
    fl_totl: float
    cat_a_sel: Optional[float] = 0.0
    cat_a_ses: Optional[float] = 0.0
    cat_a_mel: Optional[float] = 0.0
    cat_a_mes: Optional[float] = 0.0
    cat_h: Optional[float] = 0.0
    cat_g: Optional[float] = 0.0
    cat_cstm0: Optional[float] = 0.0
    cat_cstm1: Optional[float] = 0.0
    cat_cstm2: Optional[float] = 0.0
    lndgs_d: Optional[int] = 0
    lndgs_n: Optional[int] = 0
    cof_n: Optional[float] = 0.0
    cof_inst: Optional[float] = 0.0
    cof_siminst: Optional[float] = 0.0
    cof_app_n: Optional[int] = 0
    cof_app_typ: Optional[str] = None
    flight_sim: Optional[float] = 0.0
    tpt_cc: Optional[float] = 0.0
    tpt_solo: Optional[float] = 0.0
    tpt_pic: Optional[float] = 0.0
    tpt_sic: Optional[float] = 0.0
    tpt_dual: Optional[float] = 0.0
    tpt_cfi: Optional[float] = 0.0
    notes: Optional[str] = None


class FlightCreate(FlightBase):
    pass


class Flight(FlightBase):

    class Config:
        orm_mode = True
    pass
