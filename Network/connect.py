import json

import subprocess
from . import models
from . import hash


def connect_open(config: models.NoSecurity):

    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_leap(config: models.LEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.leapusername,
        "802-1x.password", config.leappassword
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpapersonal(config: models.WpaPersonal):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterpriseTLS(config: models.WpaEnterpriseTLS):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "tls",
        "802-1x.identity", config.tlsid,
        "802-1x.client-cert", "/path/to/client-cert.pem",
        "802-1x.private-key", "/path/to/private-key.pem",
    ]

    if not config.nocacert:
        cmd += ["802-1x.ca-cert", "/path/to/ca-cert.pem"]

    if config.userPKpassword:
        cmd += ["802-1x.private-key-password", config.userPKpassword]

    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterpriseLEAP(config: models.WpaEnterpriseLEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.leapusername,
        "802-1x.password", config.leappassword
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterprisePWD(config: models.WpaEnterprisePWD):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "peap",
        "802-1x.identity", config.pwdusername,
        "802-1x.password", config.pwdpassword
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterpriseFAST(config: models.WpaEnterpriseFAST):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "fast",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterpriseTTLS(config: models.WpaEnterpriseTTLS):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "ttls",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.ca_cert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpaenterprisePEAP(config: models.WpaEnterprisePEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "peap",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.ca_cert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_wpa3(config: models.Wpa3):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}

def connect_eopen(config: models.Eopen):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname
    ]
    try:
        subprocess.run(cmd, check=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": str(e)}