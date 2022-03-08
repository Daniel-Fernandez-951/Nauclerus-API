import datetime
import uuid

from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import (Column, ForeignKey,
                        Integer, String,
                        Date, Numeric,
                        Boolean, DateTime)

# Local import
from app.database.configuration import Base


def _get_date():
    return datetime.datetime.now().date()


def _get_year():
    return datetime.datetime.now().year


class Pilot(Base):
    __tablename__ = "pilots"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    rec_flights = relationship("Flight", back_populates="pilot_flights")
    piloted_ac = relationship("Aircraft", back_populates="pilot_ac")


class Logbook(Base):
    __tablename__ = "logbook"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)
    pilot_id = Column(UUID, ForeignKey("pilots.id"))
    logbook_style = Column(String, nullable=False, unique=True)
    header_titles = Column(JSONB)


class Aircraft(Base):
    # TODO: Is it AIRPLANE, HELI, GLIDER, LS, etc.
    __tablename__ = "aircraft"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)
    pilot_id = Column(UUID, ForeignKey("pilots.id"))
    ac_tail = Column(String, nullable=False)
    ac_mm = Column(String, nullable=False)
    is_retractable = Column(Boolean, default=False)

    pilot_ac = relationship("Pilot", back_populates="piloted_ac")


class Flight(Base):
    __tablename__ = "flights"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid.uuid4,
                nullable=False, unique=True,
                autoincrement=False)

    pilot_id = Column(UUID, ForeignKey("pilots.id"))
    aircraft_id = Column(UUID, ForeignKey("aircraft.id"))

    year = Column(Integer, default=_get_year, index=True)
    date = Column(Date, default=_get_date, index=True)
    fl_from = Column(String)
    fl_to = Column(String)
    fl_totl = Column(Numeric(4, 2), default=None, nullable=True)
    cat_a_sel = Column(Numeric(4, 2), default=0)
    cat_a_ses = Column(Numeric(4, 2), default=0)
    cat_a_mel = Column(Numeric(4, 2), default=0)
    cat_a_mes = Column(Numeric(4, 2), default=0)
    cat_h = Column(Numeric(4, 2), default=0)
    cat_g = Column(Numeric(4, 2), default=0)
    cat_cstm0 = Column(Numeric(4, 2), default=0)
    cat_cstm1 = Column(Numeric(4, 2), default=0)
    cat_cstm2 = Column(Numeric(4, 2), default=0)
    cof_n = Column(Numeric(4, 2), default=0)
    cof_inst = Column(Numeric(4, 2), default=0)
    cof_siminst = Column(Numeric(4, 2), default=0)
    flight_sim = Column(Numeric(4, 2), default=0)
    tpt_cc = Column(Numeric(4, 2), default=0)
    tpt_solo = Column(Numeric(4, 2), default=0)
    tpt_pic = Column(Numeric(4, 2), default=0)
    tpt_sic = Column(Numeric(4, 2), default=0)
    tpt_dual = Column(Numeric(4, 2), default=0)
    tpt_cfi = Column(Numeric(4, 2), default=0)
    notes = Column(String, nullable=True)
    lndgs_d = Column(Integer, default=0)
    lndgs_n = Column(Integer, default=0)
    cof_app_n = Column(Integer, default=0)
    cof_app_typ = Column(String, default=None, nullable=True)

    # Relationships
    pilot_flights = relationship("Pilot", back_populates="rec_flights")
