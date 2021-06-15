"""
Source: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-database-url-for-sqlalchemy
"""

import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.orm import relationship

# Local import
from .database import Base


def _get_date():
    return datetime.datetime.now().date()


class Pilot(Base):
    # TODO: Add more features to pilot?
    __tablename__ = "pilot"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)


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
    sel_t = Column(Numeric(3, 2), default=0)
    mel_t = Column(Numeric(3, 2), default=0)

    cross_c = Column(Numeric(3, 2), default=0)
    # Conditions of flight
    day = Column(Numeric(3, 2), default=0)
    night = Column(Numeric(3, 2), default=0)
    actual_inst = Column(Numeric(3, 2), default=0)
    sim_inst = Column(Numeric(3, 2), default=0)

    ground_train = Column(Numeric(3, 2), default=0)
    # Type of piloting time
    dual_rec = Column(Numeric(3, 2), default=0)
    pic = Column(Numeric(3, 2), default=0)
    # Total flight time
    ft_total = Column(Numeric(3, 2), default=0)

    # TODO: Add relationships for Flights


