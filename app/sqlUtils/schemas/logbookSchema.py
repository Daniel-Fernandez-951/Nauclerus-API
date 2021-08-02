import inspect
from pydantic import BaseModel, BaseConfig


def stringify(*fields):
    def dec(_cls):
        for field in fields:
            _cls.__fields__[field].required = False
        return _cls
    if fields and inspect.isclass(fields[0]) and issubclass(fields[0], BaseModel):
        cls = fields[0]
        fields = cls.__fields__
        return dec(cls)


@stringify
class LogbookMap(BaseModel):

    class Config:
        orm_mode = True

    ac_tail: str
    ac_mm: str
    year: str
    date: str
    fl_from: str
    fl_to: str
    fl_totl: str
    cat_a_sel: str
    cat_a_ses: str
    cat_a_mel: str
    cat_a_mes: str
    cat_h: str
    cat_g: str
    cat_cstm0: str
    cat_cstm1: str
    cat_cstm2: str
    lndgs_d: str
    lndgs_n: str
    cof_n: str
    cof_inst: str
    cof_siminst: str
    cof_app_n: str
    cof_app_typ: str
    flight_sim: str
    tpt_cc: str
    tpt_solo: str
    tpt_pic: str
    tpt_sic: str
    tpt_dual: str
    tpt_cfi: str
    notes: str


class LogbookBase(BaseModel):
    pilot_id: int
    logbook_style: str
    header_titles: LogbookMap


class LogbookCreate(LogbookBase):
    pass


class Logbook(LogbookBase):
    id: int
