""" setup hub wifi

Antony Wiegand, McMaster, 2026
"""

from pathlib import Path
import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import apmode
from . import hash
from . import models
from . import connect

# uvicorn Network.main:network --host 0.0.0.0 --port 8080 --reload

BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"

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


def load_credentials() -> list:
    """Load saved encrypted credentials"""
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_credentials(entry: dict) -> None:
    """Save encrypted credentials"""
    stored = load_credentials()
    stored.append(entry)

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(stored, f, indent=2)


def connect_wifi(data: models.WifiPayload):
    """Connect using the already-validated Pydantic model"""

    connect_map = {
        "open": connect.connect_open,
        "wpa_personal": connect.connect_wpapersonal,
        "wpa3personal": connect.connect_wpa3,
        "leap": connect.connect_leap,
        "eopen": connect.connect_eopen,
        "wpa_enterprise_tls": connect.connect_wpaenterpriseTLS,
        "wpa_enterprise_leap": connect.connect_wpaenterpriseLEAP,
        "wpa_enterprise_pwd": connect.connect_wpaenterprisePWD,
        "wpa_enterprise_fast": connect.connect_wpaenterpriseFAST,
        "wpa_enterprise_peap": connect.connect_wpaenterprisePEAP,
        "wpa_enterprise_ttls": connect.connect_wpaenterpriseTTLS,
    }

    func = connect_map.get(data.type)
    if func is None:
        raise HTTPException(status_code=400, detail=f"Unsupported wifi type: {data.type}")

    return func(data)


@network.post("/wifi")
def save_wifi(data: models.WifiPayload):
    """Save wifi credentials and try connecting"""

    wifi_dict = data.model_dump()
    encrypted_entry = hash.encrypt_data(wifi_dict)

    save_credentials(
        {
            "security": data.type,
            "encrypted": encrypted_entry,
        }
    )

    result = connect_wifi(data)

    if result.get("status") == "connected":
        apmode.stop_ap_mode()

    return {
        "status": "saved",
        "connection": result,
    }


network.mount("/", StaticFiles(directory=str(BASE_DIR), html=True), name="setup")