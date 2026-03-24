""" setup hub wifi

Antony Wiegand, McMaster, 2026"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json

from . import apmode
from . import hash
from . import models
from . import connect

# uvicorn Network.main:network --host 0.0.0.0 --port 8080 --reload

network = FastAPI()

network.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@network.on_event("startup")
def startup():
    apmode.start_ap_mode()

@network.post("/wifi")
def save_wifi(data: models.WifiPayload):
    """Save wifi credentials"""

    wifi_dict = data.dict()
    security_type = wifi_dict["type"]

    encrypted_entry = hash.encrypt_data(wifi_dict)

    try:
        with open("Network/credentials.json", "r") as f:
            stored = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        stored = []

    stored.append({"security": security_type,
                   "encrypted": encrypted_entry})

    with open("Network/credentials.json", "w") as f:
        json.dump(stored, f, indent=2)
    
    try:
        result = connect_wifi(data)
    finally:
        apmode.stop_ap_mode()


    return {"status": "saved", "connection":result}



def connect_wifi(data: models.WifiPayload):

    with open("Network/credentials.json", "r") as f:
        stored = json.load(f)

        entry = stored[-1]
        
        unencrypted_creds = hash.unencrypt_data(entry["encrypted"])

        connect_map = {
        "open": connect.connect_open,
        "wpa_personal": connect.connect_wpapersonal,
        "wpa3": connect.connect_wpa3,
        "leap": connect.connect_leap,
        "eopen": connect.connect_eopen,
        "wpa_enterprise_tls": connect.connect_wpaenterpriseTLS,
        "wpa_enterprise_leap": connect.connect_wpaenterpriseLEAP,
        "wpa_enterprise_pwd": connect.connect_wpaenterprisePWD,
        "wpa_enterprise_fast": connect.connect_wpaenterpriseFAST,
        "wpa_enterprise_peap": connect.connect_wpaenterprisePEAP,
        "wpa_enterprise_ttls": connect.connect_wpaenterpriseTTLS
        }

    func = connect_map.get(unencrypted_creds["type"], connect.connect_open)
    return func(unencrypted_creds)


network.mount("/", StaticFiles(directory="Network", html=True), name="setup")