""" Table & Schema formats

All table & schema formats needed

Antony Wiegand, McMaster, 2026"""

from sqlmodel import Field, SQLModel
from datetime import date

class Sensor(SQLModel, table=True):
    """
    Table containing (in this order):
    - id (int) (primary-key)
    - sensor_id (str)
    - moisture (float)
    - temperature (float)
    - humidity (float)
    - timestamp (date: YYYY,MM,DD) (auto-added) \n
    Gives Ability to select by date.
    """
    id: int | None = Field(default=None, primary_key=True)
    sensor_id: str
    moisture: float
    temperature: float
    humidity: float
    timestamp: date = Field(default_factory=date.today)

class CreateSensor(SQLModel):
    """
    Schema containing (in this order):
    - sensor_id (str)
    - moisture (float)
    - temperature (float)
    - humidity (float) \n
    Used only for adding data.
    """
    sensor_id: str
    moisture: float
    temperature: float
    humidity: float

class Guidebook(SQLModel, table=True):
    
    id: int | None = Field(default=None, primary_key=True)
    name : str | None = None
    tips: str | None = None
    opt_temperature_low: float | None = None
    opt_temperature_high: float | None = None
    opt_humidity_low: float | None = None
    opt_humidity_high: float | None = None
    opt_moisture_low: float | None = None
    opt_moisture_high: float | None = None
    image_url: str | None = None



# do we need indexes? its just adding = Field(index=True)