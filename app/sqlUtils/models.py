"""
Source: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-database-url-for-sqlalchemy
"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship

# Local import
from sqlUtils.database import Base


def _get_date():
    return datetime.datetime.now().date()


def _get_year():
    return datetime.datetime.now().year


class Pilot(Base):
    # TODO: Add more features to pilot?
    __tablename__ = "pilots"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    rec_flights = relationship("Flight", back_populates="pilot_flights")
    piloted_ac = relationship("Aircraft", back_populates="pilot_ac")


class Aircraft(Base):
    # TODO: More features for airplane?
    __tablename__ = "planes"

    id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilots.id"))
    tail_num = Column(String, unique=True)

    pilot_ac = relationship("Pilot", back_populates="piloted_ac")


class Flight(Base):
    # TODO: This represents one style of US logbook (ASA-SP-40)
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    # Linked info plane/pilot
    pilot = Column(Integer, ForeignKey("pilots.id"))
    aircraft = Column(Integer, ForeignKey("planes.id"))
    # Flight string info
    flight_dt = Column(Date, default=_get_date, index=True)
    flight_yr = Column(Integer, default=_get_year, index=True)
    dest_t = Column(String, nullable=False)
    dest_f = Column(String, nullable=False)
    notes = Column(String)
    # Flight numerical info
    ifr_app = Column(Integer, default=0)
    landings = Column(Integer, default=1)
    # Aircraft Category
    sel_t = Column(Numeric(4, 2), default=0)
    mel_t = Column(Numeric(4, 2), default=0)

    cross_c = Column(Numeric(4, 2), default=0)
    # Conditions of flight
    day = Column(Numeric(4, 2), default=0)
    night = Column(Numeric(4, 2), default=0)
    actual_inst = Column(Numeric(4, 2), default=0)
    sim_inst = Column(Numeric(4, 2), default=0)

    ground_train = Column(Numeric(3, 2), default=0)
    # Type of piloting time
    dual_rec = Column(Numeric(3, 2), default=0)
    pic = Column(Numeric(3, 2), default=0)
    # Total flight time
    ft_total = Column(Numeric(3, 2), default=0)

    # Relationships
    pilot_flights = relationship("Pilot", back_populates="rec_flights")
