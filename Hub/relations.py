""" Table functions

Gives the ability to add to, take from, or delete from a table

Antony Wiegand, McMaster, 2026"""

from sqlmodel import Session, select, delete
from datetime import date
from statistics import median

from . import models
from . import db

def create_sensors(sensor: models.CreateSensor):
    """
    Input: JSON file (alternative table format)
    1. Opens (and closes once done) a task session
    2. Converts JSON file into main table format (adds id-key & timestamp)
    3. Adds data to the table
    4. Saves and refreshes \n
    Output: None
    """
    with Session(db.engine) as session:
        sensor_db = models.Sensor(**sensor.model_dump())
        session.add(sensor_db)
        session.commit()
        session.refresh(sensor_db)

def select_sensors(date: date, sensor_id: str):
    """
    Input: Date (YYYY,MM,DD)
    1. Opens (and closes once done) a task session
    2. Finds and selects all sensor data from given date and sensor_id
    3. Finds the median of each sensor.
    4. Saves and refreshes \n
    Output: Median sensor data from given date and sensor_id.
    """
    with Session(db.engine) as session:
        statement = select(models.Sensor).where((models.Sensor.timestamp.like(f"{date}%")) & (models.Sensor.sensor_id == sensor_id))
        results = session.exec(statement)
        sensors = results.all()

        m = [r.moisture for r in sensors]
        t = [r.temperature for r in sensors]
        h = [r.humidity for r in sensors]

        median_m = median(m)
        median_t = median(t)
        median_h = median(h)

        return {
            "moisture": median_m,
            "temperature": median_t,
            "humidity": median_h
        }

def delete_sensors(date: date):
    """
    Input: Date (YYYY,MM,DD)
    1. Opens (and closes once done) a task session
    2. Finds and deletes all sensor data from given date
    3. Saves and refreshes \n
    Output: None
    """
    with Session(db.engine) as session:
        statement = delete(models.Sensor).where(models.Sensor.timestamp <= date) # <--CHECK IF THIS ACTUALLY WORKS
        session.exec(statement)
        session.commit()