"""
Source: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-database-url-for-sqlalchemy
"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date, FLOAT
from sqlalchemy.orm import relationship

# Local import
from .database import Base


def _get_date():
    return datetime.datetime.now().date()


class Pilot(Base):
    # TODO: Add more features to pilot?
    __tablename__ = "pilot"

    id = Column(Integer, primary_key=True, index=True)

    # TODO: Add relationships for Pilot
    # piloted_ac = relationship("Aircraft", back_populates=)
    # rec_flights = relationship("Flight", back_populates=)


class Aircraft(Base):
    # TODO: More features for airplane?
    __tablename__ = "plane"

    id = Column(Integer, primary_key=True, index=True)
    pilot_id = Column(Integer, ForeignKey("pilot.id"))
    tail_num = Column(String, unique=True)

    # TODO: Add relationships for Aircraft
    # ac_flights = relationship("Flight", back_populates=)
    # ac_pilot = relationship("Pilot", back_populates=)


class Flight(Base):
    # TODO: This represents one style of US logbook (ASA-SP-40)
    __tablename__ = "flight"

    id = Column(Integer, primary_key=True, index=True)
    # Linked info plane/pilot
    pilot = Column(Integer, ForeignKey("pilot.id"))
    aircraft = Column(Integer, ForeignKey("plane.id"))
    # Flight string info
    flight_dt = Column(Date, default=_get_date)
    dest_t = Column(String(4), nullable=False)
    dest_f = Column(String(4), nullable=False)
    notes = Column(String(128))
    # Flight numerical info
    ifr_app = Column(Integer(2), default=0)
    landings = Column(Integer(2), default=1)
    # Aircraft Category
    sel_t = Column(FLOAT(precision=4), default=0)
    mel_t = Column(FLOAT(precision=4), default=0)

    cross_c = Column(FLOAT(precision=4), default=0)
    # Conditions of flight
    day = Column(FLOAT(precision=4), default=0)
    night = Column(FLOAT(precision=4), default=0)
    actual_inst = Column(FLOAT(precision=4), default=0)
    sim_inst = Column(FLOAT(precision=4), default=0)

    ground_train = Column(FLOAT(precision=4), default=0)
    # Type of piloting time
    dual_rec = Column(FLOAT(precision=4), default=0)
    pic = Column(FLOAT(precision=4), default=0)
    # Total flight time
    ft_total = Column(FLOAT(precision=4), default=0)

    # TODO: Add relationships for Flights


