from pydantic import BaseModel


# Aircraft
class AircraftBase(BaseModel):
    ac_tail: str
    ac_mm: str


class AircraftCreate(AircraftBase):
    is_retractable: bool = False


# Reading and Returning Section
class Aircraft(AircraftBase):
    id: int
    pilot_id: int
    is_retractable: bool

    class Config:
        orm_mode = True
