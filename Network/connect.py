import subprocess
from . import models


def run_nmcli(cmd: list[str]):
    """Run nmcli and return a simple result dict."""
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return {"status": "connected"}
    except subprocess.CalledProcessError as e:
        return {
            "status": "failed",
            "error": e.stderr.strip() if e.stderr else str(e)
        }


def connect_open(config: models.NoSecurity):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname
    ]
    return run_nmcli(cmd)


def connect_leap(config: models.LEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.username,
        "802-1x.password", config.password
    ]
    return run_nmcli(cmd)


def connect_wpapersonal(config: models.WpaPersonal):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ]
    return run_nmcli(cmd)


def connect_wpa3(config: models.Wpa3):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ]
    return run_nmcli(cmd)


def connect_eopen(config: models.Eopen):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname
    ]
    return run_nmcli(cmd)


def connect_wpaenterpriseTLS(config: models.WpaEnterpriseTLS):
    cmd = [
        "nmcli", "connection", "add",
        "type", "wifi",
        "ifname", "*",
        "con-name", config.wifiname,
        "ssid", config.wifiname,
        "wifi-sec.key-mgmt", "wpa-eap",
        "802-1x.eap", "tls",
        "802-1x.identity", config.tlsid,
    ]

    if config.domain:
        cmd += ["802-1x.domain-suffix-match", config.domain]

    if config.ca_cert and not config.nocacert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    if config.usercertpassword:
        cmd += ["802-1x.client-cert-password", config.usercertpassword]

    if config.userPKpassword:
        cmd += ["802-1x.private-key-password", config.userPKpassword]

    return run_nmcli(cmd)


def connect_wpaenterpriseLEAP(config: models.WpaEnterpriseLEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.leapusername,
        "802-1x.password", config.leappassword
    ]
    return run_nmcli(cmd)


def connect_wpaenterprisePWD(config: models.WpaEnterprisePWD):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "pwd",
        "802-1x.identity", config.pwdusername,
        "802-1x.password", config.pwdpassword
    ]
    return run_nmcli(cmd)


def connect_wpaenterpriseFAST(config: models.WpaEnterpriseFAST):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "fast",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.innerauth:
        cmd += ["802-1x.phase2-auth", config.innerauth]

    return run_nmcli(cmd)


def connect_wpaenterpriseTTLS(config: models.WpaEnterpriseTTLS):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "ttls",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.innerauth:
        cmd += ["802-1x.phase2-auth", config.innerauth]

    if config.domain:
        cmd += ["802-1x.domain-suffix-match", config.domain]

    if config.ca_cert and not config.noncacert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    return run_nmcli(cmd)


def connect_wpaenterprisePEAP(config: models.WpaEnterprisePEAP):
    cmd = [
        "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "peap",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.innerauth:
        cmd += ["802-1x.phase2-auth", config.innerauth]

    if config.domain:
        cmd += ["802-1x.domain-suffix-match", config.domain]

    if config.ca_cert and not config.noncacert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    return run_nmcli(cmd)