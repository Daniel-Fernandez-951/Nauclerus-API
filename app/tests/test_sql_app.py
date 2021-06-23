import os
import datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlUtils.database import Base
from main import get_db, app


SQLALCHMY_TEST_DB = "sqlite:///./tests/test.db"

engine = create_engine(
    SQLALCHMY_TEST_DB, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_pilot():
    pilot_name = "Biden 25th Amendment"
    response = client.post(
        "/pilot/",
        json={
            "name": f"{pilot_name}"
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data['name'] == pilot_name
    assert data["id"] == 1
    user_id = data["id"]
    test_name = data["name"]

    response = client.get(f"/pilot/{user_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == test_name
    assert data["rec_flights"] == []
    assert data["piloted_ac"] == []


def test_get_fake_pilot():
    response = client.get(f"/pilot/88")

    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Pilot with ID does not exist"


def test_create_aircraft():
    fake_tail_num = 'N123W'
    user_id = 1
    response = client.post(
        f"/aircraft/{user_id}",
        json={
            "tail_num": f"{fake_tail_num}"
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["tail_num"] == fake_tail_num
    assert data["pilot_id"] == user_id
    assert type(data["id"]) == int


def test_create_flight():
    pilot_id = 1
    aircraft_id = 1
    airport = "KSFO"

    response = client.post(
        f"/flight/?pilot_id={pilot_id}&aircraft_id={aircraft_id}",
        json={
            "flight_dt": f"{datetime.datetime.now().date()}",
            "flight_yr": f"{datetime.datetime.now().year}",
            "dest_t": f"{airport}",
            "dest_f": f"{airport}",
            "notes": "",
            "ifr_app": 0,
            "landings": 1,
            "sel_t": 0,
            "mel_t": 0,
            "cross_c": 0,
            "day": 0,
            "night": 0,
            "actual_inst": 0,
            "sim_inst": 0,
            "ground_train": 0,
            "dual_rec": 0,
            "pic": 0,
            "ft_total": 1.0
        },
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert data["pilot"] == pilot_id
    assert data["aircraft"] == aircraft_id
    assert data["dest_f"] == airport


def test_clean_up():
    os.remove("./tests/test.db")
    return "Success"
