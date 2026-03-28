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

def run_cmd(cmd: list[str]):
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True
        )
        return {
            "success": True,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()
        }
    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "stdout": e.stdout.strip() if e.stdout else "",
            "stderr": e.stderr.strip() if e.stderr else str(e)
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
    con_name = "Reznet-WiFi"

    result = run_nmcli([
        "nmcli","connection","add",
        "type","wifi",
        'ifname','wlan0',
        'con-name',con_name,
        "ssid",config.wifiname
    ])

    if result["status"] == "failed":
        return result

    cmd = [
        "nmcli", "connection", 'modify', con_name,
        "wifi-sec.key-mgmt", "wpa-eap",
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

    result = run_nmcli(cmd)
    if result["status"] == "failed":
        return result
    
    connect = ["nmcli", "connection", "up", con_name, 'ifname', 'wlan0']

    return run_nmcli(connect)

def disconnect_wifi(ifname: str = "wlan0"):
    result = run_cmd(["nmcli","device","disconnect",ifname])

    if result.returncode == 0:
        print(f"{ifname} disconnected from Wifi")
        return True
    
    err = (result.stderr or "").strip().lower()

    if "not connected" in err or "disconnected" in err:
        print(f"{ifname} was already disconnected")
        return True
    
    print(f"Failed to disconnect {ifname}: {result.stderr}")
    return False