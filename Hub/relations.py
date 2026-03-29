""" Table functions

Gives the ability to add to, take from, or delete from a table

Antony Wiegand, McMaster, 2026"""

from sqlmodel import Session, select, delete
from datetime import date
from statistics import mean, median, StatisticsError

from . import models
from . import db

COMPARISONREADINGS = 6
MAXTEMPVARIANCE = 5
MAXHUMIDVARIANCE = 20

tempdeltas = []
for j in range (0, COMPARISONREADINGS - 1):
    tempdeltas.append (None)

humiddeltas = []
for l in range (0, COMPARISONREADINGS - 1):
    humiddeltas.append(None)


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
        statement = select(models.Sensor).where(
            (models.Sensor.timestamp.like(f"{date}%")) &
            (models.Sensor.sensor_id == sensor_id)
        ).limit(COMPARISONREADINGS)
        sensors = session.exec(statement).all()

        m = [r.moisture for r in sensors]
        t = [r.temperature for r in sensors]
        h = [r.humidity for r in sensors]

        # compute median safely
        try:
            median_m = median(m)
        except StatisticsError:
            median_m = None

        try:
            for datapoint in range (1, COMPARISONREADINGS - 1):
                tempdelta[datapoint] = t[datapoint] - t[datapoint + 1]

            tempprediction = t[1] + statistics.mean(tempdeltas)

            if abs(t[0] - tempprediction) > MAXTEMPVARIANCE:
                validated_t = None
            else:
                validated_t = t[0]
        except StatisticsError:
            median_t = None

        try:
            for datapoint in range (1, COMPARISONREADINGS - 1):
                humiddelta[datapoint] = h[datapoint] - h[datapoint + 1]

            humidprediction = h[1] + statistics.mean(humiddeltas)

            if abs(h[0] - humidprediction) > MAXHUMIDVARIANCE:
                validated_h = None
            else:
                validated_h = h[0]
        except StatisticsError:
            median_h = None

        return {
            "moisture": median_m,
            "temperature": validated_t,
            "humidity": validated_h
        }

def select_guide(id: int):

    with Session(db.engine) as session:
        statement = select(models.Guidebook).where((models.Guidebook.id == id))
        result = session.exec(statement)
        plant = result.first()

        return {
            "id": plant.id,
            "name": plant.name,
            "tips": plant.tips,
            "opt_temperature_low": plant.opt_temperature_low,
            "opt_temperature_high": plant.opt_temperature_high,
            "opt_humidity_low": plant.opt_humidity_low,
            "opt_humidity_high": plant.opt_humidity_high,
            "opt_moisture_low": plant.opt_moisture_low,
            "opt_moisture_high": plant.opt_moisture_high,
            "image_url": plant.image_url
        }
    
def select_all_guides():
    with Session(db.engine) as session:
        statement = select(models.Guidebook)
        result = session.exec(statement)
        plant = result.all()

    return plant


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
