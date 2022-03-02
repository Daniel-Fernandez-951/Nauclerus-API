from pydantic import BaseModel, UUID4
from typing import Optional


class LogbookMap(BaseModel):
    class Config:
        orm_mode = True

    ac_tail: Optional[str] = "Aircraft Tail Number"
    ac_mm: Optional[str] = "Aircraft Make and Model"
    year: Optional[str] = "Flight Year"
    date: Optional[str] = "Flight Date"
    fl_from: Optional[str] = "Flight From"
    fl_to: Optional[str] = "Flight To"
    fl_totl: Optional[str] = "Total Flight Time"
    cat_a_sel: Optional[str] = "Category SE Land"
    cat_a_ses: Optional[str] = "Category SE Sea"
    cat_a_mel: Optional[str] = "Category ME Land"
    cat_a_mes: Optional[str] = "Category ME Sea"
    cat_h: Optional[str] = "Category Helicopter"
    cat_g: Optional[str] = "Category Glider"
    cat_cstm0: Optional[str] = "Category Custom 0"
    cat_cstm1: Optional[str] = "Category Custom 1"
    cat_cstm2: Optional[str] = "Category Custom 2"
    lndgs_d: Optional[str] = "Day Landings"
    lndgs_n: Optional[str] = "Night Landings"
    cof_n: Optional[str] = "Condition of Flight - Night"
    cof_inst: Optional[str] = "Condition of Flight - Instrument"
    cof_siminst: Optional[str] = "Condition of Flight - Simulated Instrument"
    cof_app_n: Optional[str] = "Condition of Flight - Night Approach"
    cof_app_typ: Optional[str] = "Condition of Flight - Approach Type"
    flight_sim: Optional[str] = "Flight Simulator"
    tpt_cc: Optional[str] = "Type of Piloting Time - Cross Country"
    tpt_solo: Optional[str] = "Type of Piloting Time - Solo"
    tpt_pic: Optional[str] = "Type of Piloting Time - Pilot in Command"
    tpt_sic: Optional[str] = "Type of Piloting Time - Second in Command"
    tpt_dual: Optional[str] = "Type of Piloting Time - Dual"
    tpt_cfi: Optional[str] = "Type of Piloting Time - Certified Flight Instructor"
    notes: Optional[str] = "Notes"


class LogbookBase(BaseModel):
    pilot_id: Optional[str] = "Overridden"
    logbook_style: str = "Name this logbook map"
    header_titles: LogbookMap


class LogbookCreate(LogbookBase):
    pass


class Logbook(LogbookBase):
    id: Optional[UUID4]
