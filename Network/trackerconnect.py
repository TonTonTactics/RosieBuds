from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time

from . import apmode
from . import models
from . import connect

tracker = FastAPI()

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

def connect_to_home_wifi(data: models.WifiPayload):
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

    return func(data)

def timeout_provision():
    """
    Wait 30 seconds. If tracker has not connected,
    stop AP mode and return to normal Wi-Fi.
    """
    time.sleep(30)

    if provision_state["state"] == "waiting_for_tracker":
        print("Provisioning timed out.")

        apmode.stop_ap_mode()
        provision_state["state"] = "returning_to_wifi"

        connect_to_home_wifi()

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

    return {
        "ok": True,
        "ssid": provision_state["ssid"],
        "password": provision_state["password"],
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
    provision_state["state"] = "returning_to_wifi"

    connect_to_home_wifi()

    provision_state["state"] = "tracker_confirmed"
    provision_state["active"] = False

    print(f"Tracker {data.tracker_id} finished setup.")

    return {
        "ok": True,
        "state": provision_state["state"],
    }

# uvicorn Network.trackerconnect:tracker --host 0.0.0.0 --port 9000 --reload