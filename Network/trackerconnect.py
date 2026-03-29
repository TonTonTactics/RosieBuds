from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time
from fastapi.middleware.cors import CORSMiddleware
import json
import threading

from . import apmode
from . import models
from . import connect
from . import hash

tracker = FastAPI()

tracker.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://0.0.0.0:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


provision_state = {
    "active": False,
    "state": "idle",
    "tracker_id": None,
    "ssid": "YourHomeWiFi",
    "password": "YourPassword",
    "hub_ip": "192.168.1.50",
    "hub_port": 9000,
}

class ClaimRequest(BaseModel):
    tracker_id: str

class CompleteRequest(BaseModel):
    tracker_id: str
    status: str

def load_home_wifi():
    with open("Network/credentials.json","r",encoding="utf-8") as f:
        data = json.load(f)

        if not data:
            return None
        
        last_entry = data[-1]

        encrypted= last_entry.get("encrypted")
        security = last_entry.get("security")

        if not encrypted:
            raise ValueError(f"No encrypted value found in lastentry: {last_entry}")
        
        wifi_data = hash.decrypt_data(encrypted)

    return {
        "security":security,
        "credentials":wifi_data
    }


def connect_to_home_wifi(data: models.WifiPayload):
    """Connect using the already-validated Pydantic model"""

    data = load_home_wifi()

    if not data:
         return {"status": "failed", "error": "No saved home wifi"}

    security = data["security"]
    creds = data["credentials"]

    if "ssid" in creds and "wifiname" not in creds:
        creds["wifiname"] = creds["ssid"]

    connect_map = {
        "open": lambda c:connect.connect_open(models.NoSecurity(**c)),
        "wpa_personal": lambda c: connect.connect_wpapersonal(models.WpaPersonal(**c)),
        "wpa3personal": lambda c: connect.connect_wpa3(models.Wpa3(**c)),
        "leap": lambda c: connect.connect_leap(models.LEAP(**c)),
        "eopen": lambda c: connect.connect_eopen(models.Eopen(**c)),
        "wpa_enterprise_tls": lambda c: connect.connect_wpaenterpriseTLS(models.WpaEnterpriseTLS(**c)),
        "wpa_enterprise_leap": lambda c: connect.connect_wpaenterpriseLEAP(models.WpaEnterpriseLEAP(**c)),
        "wpa_enterprise_pwd": lambda c: connect.connect_wpaenterprisePWD(models.WpaEnterprisePWD(**c)),
        "wpa_enterprise_fast": lambda c: connect.connect_wpaenterpriseFAST(models.WpaEnterpriseFAST(**c)),
        "wpa_enterprise_peap": lambda c: connect.connect_wpaenterprisePEAP(models.WpaEnterprisePEAP(**c)),
        "wpa_enterprise_ttls": lambda c: connect.connect_wpaenterpriseTTLS(models.WpaEnterpriseTTLS(**c)),
    }

    connect_fn=connect_map.get(security)
    if not connect_fn:
        return {"status": "Failed","error":f"Unsupported security: {security}"}
    return connect_fn(creds)

def timeout_provision():
    """
    Wait 30 seconds. If tracker has not connected,
    stop AP mode and return to normal Wi-Fi.
    """
    time.sleep(60)

    if provision_state["state"] == "waiting_for_tracker":
        print("Provisioning timed out.")

        apmode.stop_ap_mode()

        wifi=load_home_wifi()
        connect_to_home_wifi(wifi)

        provision_state["state"] = "timeout"
        provision_state["active"] = False


@tracker.post("/provision/start")
def start_provision():
    """
    Starts a new 30-second tracker setup session.
    """
    if provision_state["active"]:
        return {
            "ok": False,
            "error": "Provisioning already active",
            "state": provision_state["state"],
        }

    provision_state["active"] = True
    provision_state["state"] = "ap_mode"
    provision_state["tracker_id"] = None

    apmode.stop_ap_mode()

    apmode.start_ap_mode()

    provision_state["state"] = "waiting_for_tracker"

    timer_thread = threading.Thread(target=timeout_provision, daemon=True)
    timer_thread.start()

    return {
        "ok": True,
        "state": provision_state["state"],
        "message": "Hub AP mode started. Waiting for tracker.",
    }


@tracker.get("/provision/status")
def get_provision_status():
    """
    Used by the webapp to poll current pairing status.
    """
    return {
        "active": provision_state["active"],
        "state": provision_state["state"],
        "tracker_id": provision_state["tracker_id"],
    }

@tracker.get("/provision/credentials")
def get_provision_credentials():
    if not provision_state["active"]:
        return {
            "ok": False,
            "error": "No saved home Wi-Fi credentials"
        }
    
    wifi = load_home_wifi()
    if not wifi:
        return {
            "ok": False,
            "error": "No saved home Wi-Fi credentials"
        }
    
    creds = wifi["credentials"]

    def switch_back():
        time.sleep(2)
        apmode.stop_ap_mode()
        connect.connect_home_wifi_ap()

    threading.Thread(target=switch_back, daemon=True).start()

    return {
        "ok": True,
        "ssid": creds.get("ssid") or creds.get("wifiname"),
        "password": creds.get("password",""),
        "hub_ip": provision_state["hub_ip"],
        "hub_port": provision_state["hub_port"],
    }


@tracker.post("/provision/claim")
def claim_provision(data: ClaimRequest):
    """
    Called by the tracker after it connects to the Hub AP.
    The Hub returns the Wi-Fi credentials the tracker should use.
    """
    if not provision_state["active"]:
        return {
            "ok": False,
            "error": "No active provisioning session",
        }

    if provision_state["state"] != "waiting_for_tracker":
        return {
            "ok": False,
            "error": f"Provisioning not ready, current state: {provision_state['state']}",
        }

    provision_state["tracker_id"] = data.tracker_id
    provision_state["state"] = "tracker_connected"

    print(f"Tracker {data.tracker_id} connected to AP.")

    provision_state["state"] = "credentials_sent"

    wifi = load_home_wifi()

    return {
        "ok": True,
        "ssid": wifi.ssid,
        "password": wifi.password,
        "hub_ip": provision_state["hub_ip"],
        "hub_port": provision_state["hub_port"],
    }


@tracker.post("/provision/complete")
def complete_provision(data: CompleteRequest):
    """
    Called by the tracker after it joins the normal Wi-Fi
    and is ready to send data.
    """
    if data.tracker_id != provision_state["tracker_id"]:
        return {
            "ok": False,
            "error": "Tracker ID does not match active session",
        }

    if data.status != "connected":
        provision_state["state"] = "error"
        provision_state["active"] = False
        return {
            "ok": False,
            "error": "Tracker did not complete setup correctly",
        }

    apmode.stop_ap_mode()

    wifi = load_home_wifi()
    connect_to_home_wifi(wifi)

    provision_state["state"] = "tracker_confirmed"
    provision_state["active"] = False

    print(f"Tracker {data.tracker_id} finished setup.")

    return {
        "ok": True,
        "state": provision_state["state"],
    }

@tracker.post("/provision/cancel")
def cancel_provision():
    try:
        apmode.stop_ap_mode()
        
        result = connect_to_home_wifi()

        return {
            "status": "cancelled",
            "wifi": result
        }
    
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

# uvicorn Network.trackerconnect:tracker --host 0.0.0.0 --port 9000 --reload