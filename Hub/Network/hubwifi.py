""" setup hub wifi

Antony Wiegand, McMaster, 2026"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import subprocess

hub = FastAPI()

# uvicorn Network.hubwifi:hub --host 0.0.0.0 --port 8080

hub.mount("/", StaticFiles(directory="Network", html=True), name="setup")

class Wifi(BaseModel):
    ssid: str
    password: str

@hub.post("/wifi")
def connect_wifi(data: Wifi):

    config = f"""
network={{
    ssid="{data.ssid}"
    psk="{data.password}"
}}
"""

    with open("/etc/wpa_supplicant/wpa_supplicant.conf","a") as f:
        f.write(config)

    subprocess.run("wpa_cli", "-i", "wlan0", "reconfigure")

    return {"status":"connecting"}