""" Event to function connector

Connects Table Functions with FastAPI events.

Antony Wiegand, McMaster, 2026"""

from fastapi import FastAPI
from datetime import date
import uvicorn

from . import db
from . import relations
from . import models
from . import process

app = FastAPI()

# RUN python -m Hub.app (from outside of Hub folder)

@app.on_event("startup")
def on_startup():
    """
    Input: None
    1. Connects create database function with .onevent event "startup" \n
    Output: None
    """
    db.create_db_and_table()     # lets us use python -m Hub.app without side effects from importing

@app.post("/sensors/")
def post_sensor(sensor: models.CreateSensor):
    """
    Input: None
    1. Connects (add data) function with .post event "/sensors/" \n
    Output: None
    """
    relations.create_sensors(sensor)

@app.get("/sensors/")
def get_sensors(date: date, sensor_id: str):
    """
    Input: None
    1. Connects (grab data from date) function with .get event "/sensors/" \n
    Output: data from date
    """
    return process.rating(sensor_id, relations.select_sensors(date, sensor_id))

@app.delete("/sensors/")
def delete_sensors(date: date):
    """
    Input: None
    1. Connects (delete data from date) function with .delete event "/sensors/" \n
    Output: Confirmation of deletion
    """
    return relations.delete_sensors(date)

# allows for running python -m Hub:app
if __name__ == "__main__":
    uvicorn.run("Hub.app:app", reload= True)