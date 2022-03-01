from pydantic import BaseModel, UUID4


# Aircraft
class AircraftBase(BaseModel):
    ac_tail: str
    ac_mm: str


class AircraftCreate(AircraftBase):
    is_retractable: bool = False


# Reading and Returning Section
class Aircraft(AircraftBase):
    id: UUID4
    pilot_id: UUID4
    is_retractable: bool

    class Config:
        orm_mode = True
