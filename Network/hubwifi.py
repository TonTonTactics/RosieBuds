""" setup hub wifi

Antony Wiegand, McMaster, 2026"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


from . import security
from . import connect

hub = FastAPI()

# uvicorn Network.hubwifi:hub --host 0.0.0.0 --port 8080 --reload

class wifi(BaseModel):
    type: str
    ssid: str

    username: Optional[str] = None
    password: Optional[str] = None

    leapusername: Optional[str] = None
    leappassword: Optional[str] = None

    pwdusername: Optional[str] = None
    pwdpassword: Optional[str] = None

    anonid: Optional[str] = None
    domain: Optional[str] = None
    cacertpassword: Optional[str] = None
    noncacert: Optional[bool] = None
    nocacert: Optional[bool] = None
    innerauth: Optional[str] = None
    pacprov: Optional[str] = None

    tlsid: Optional[str] = None
    usercertpassword: Optional[str] = None
    userPKpassword: Optional[str] = None

hub.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@hub.post("/wifi")
def connect_wifi(data: wifi):
    if data.type == "open":
        config = security.Eopen(wifiname=data.ssid)
        connect.connect_open(config)

    elif data.type == "leap":
        config = security.LEAP(wifiname=data.ssid, leapusername=data.username, leappassword=data.password)
        connect.connect_leap(config)

    elif data.type == "wpa_personal":
        config = security.WpaPersonal(wifiname=data.ssid, password=data.password)
        connect.connect_wpapersonal(config)

    elif data.type == "wpa_enterprise_tls":
        config = security.WpaEnterpriseTLS(wifiname=data.ssid, tlsid=data.tlsid, domain=data.domain, cacertpassword=data.cacertpassword, nocacert=data.nocacert, usercertpassword=data.usercertpassword, userPKpassword=data.userPKpassword)
        connect.connect_wpaenterpriseTLS(config)

    elif data.type == "wpa_enterprise_leap":
        config = security.WpaEnterpriseLEAP(wifiname=data.ssid, leapusername=data.leapusername, leappassword=data.leappassword)
        connect.connect_wpaenterpriselEAP(config)

    elif data.type == "wpa_enterprise_pwd":
        config = security.WpaEnterprisePWD(wifiname=data.ssid, pwdusername=data.pwdusername, pwdpassword=data.pwdpassword)
        connect.connect_wpaenterprisePWD(config)

    elif data.type == "wpa_enterprise_fast":
        config = security.WpaEnterpriseFAST(wifiname=data.ssid, anonid=data.anonid, pacprov=data.pacprov, innerauth=data.innerauth, username=data.username, password=data.password)
        connect.connect_wpaenterpriseFAST(config)

    elif data.type == "wpa_enterprise_ttls":
        config = security.WpaEnterpriseTTLS(wifiname=data.ssid, anonid=data.anonid, domain=data.domain, cacertpassword=data.cacertpassword, noncacert=data.noncacert, innerauth=data.innerauth, username=data.username, password=data.password)
        connect.connect_wpaenterpriseTTLS(config)

    elif data.type == "wpa_enterprise_peap":
        config = security.WpaEnterprisePEAP(wifiname=data.ssid, anonid=data.anonid, domain=data.domain, cacertpassword=data.cacertpassword, noncacert=data.noncacert, innerauth=data.innerauth, username=data.username, password=data.password)
        connect.connect_wpaenterprisePEAP(config)

    elif data.type == "wpa3":
        config = security.Wpa3(wifiname=data.ssid, password=data.password)
        connect.connect_wpa3(config)

    elif data.type == "eopen":
        config = security.Eopen(wifiname=data.ssid)
        connect.connect_eopen(config)

    else:
        return {"status": "invalid wifi type"}
    

    return {"status": "connected"}

hub.mount("/", StaticFiles(directory="Network", html=True), name="setup")