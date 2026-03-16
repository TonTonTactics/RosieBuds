""" Database Creation Function

Reusable function for creating databases

Antony Wiegand, McMaster, 2026"""

from sqlmodel import SQLModel, create_engine

# REQURED DO NOT DELETE
from . import models

#name and location of database
sqlite_file_name = "/home/yusufeldar/P3-1P13-plantapp/Hub/database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# creates and connects database to location
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args) # remove echo when in production

def create_db_and_table():
    """
    Input: None
    1. Creates Database \n
    Output: None
    """
    SQLModel.metadata.create_all(engine)