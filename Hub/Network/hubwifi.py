""" setup hub wifi

Antony Wiegand, McMaster, 2026"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import subprocess
import hashlib
import binascii

hub = FastAPI()

# uvicorn Network.hubwifi:hub --host 0.0.0.0 --port 8080

hub.mount("/", StaticFiles(directory="Network", html=True), name="setup")

class Wifi(BaseModel):
    ssid: str
    password: str

@hub.post("/wifi")
def connect_wifi(data: Wifi):
    
    psk_bytes = hashlib.pbkdf2_hmac(
        "sha1",
        data.password.encode("utf-8"),
        data.ssid.encode("utf-8"),
        4096,
        32,
    )
    psk_hex = binascii.hexlify(psk_bytes).decode("ascii")

    config = f"""
network={{
    ssid="{data.ssid}"
    psk="{psk_hex}"
}}
"""

    with open("/etc/wpa_supplicant/wpa_supplicant.conf","a") as f:
        f.write(config)

    subprocess.run("wpa_cli", "-i", "wlan0", "reconfigure")

    return {"status":"connecting"}