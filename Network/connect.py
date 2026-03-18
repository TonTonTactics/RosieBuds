import subprocess
from . import security

def connect_open(config: security.NoSecurity):
    subprocess.run([
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname
    ], check=True)

def connect_leap(config: security.LEAP):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.leapusername,
        "802-1x.password", config.leappassword
    ]
    subprocess.run(cmd, check=True)

def connect_wpapersonal(config: security.WpaPersonal):
    subprocess.run([
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ], check=True)

def connect_wpaenterpriseTLS(config: security.WpaEnterpriseTLS):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "tls",
        "802-1x.identity", config.tlsid,
        "802-1x.client-cert", "/path/to/client-cert.pem",
        "802-1x.private-key", "/path/to/private-key.pem",
    ]

    if not config.nocacert:
        cmd += ["802-1x.ca-cert", "/path/to/ca-cert.pem"]

    if config.userPKpassword:
        cmd += ["802-1x.private-key-password", config.userPKpassword]

    subprocess.run(cmd, check=True)

def connect_wpaenterpriselEAP(config: security.WpaEnterpriseLEAP):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "leap",
        "802-1x.identity", config.leapusername,
        "802-1x.password", config.leappassword
    ]
    subprocess.run(cmd, check=True)

def connect_wpaenterprisePWD(config: security.WpaEnterprisePWD):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "peap",
        "802-1x.identity", config.pwdusername,
        "802-1x.password", config.pwdpassword
    ]
    subprocess.run(cmd, check=True)

def connect_wpaenterpriseFAST(config: security.WpaEnterpriseFAST):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "fast",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    subprocess.run(cmd, check=True)

def connect_wpaenterpriseTTLS(config: security.WpaEnterpriseTTLS):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "ttls",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.ca_cert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    subprocess.run(cmd, check=True)

def connect_wpaenterprisePEAP(config: security.WpaEnterprisePEAP):
    cmd = [
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "802-1x.eap", "peap",
        "802-1x.identity", config.username,
        "802-1x.password", config.password,
        "802-1x.phase2-auth", config.innerauth or "mschapv2"
    ]

    if config.anonid:
        cmd += ["802-1x.anonymous-identity", config.anonid]

    if config.ca_cert:
        cmd += ["802-1x.ca-cert", config.ca_cert]

    subprocess.run(cmd, check=True)

def connect_wpa3(config: security.Wpa3):
    subprocess.run([
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname,
        "password", config.password
    ], check=True)

def connect_eopen(config: security.Eopen):
    subprocess.run([
        "sudo", "nmcli", "dev", "wifi", "connect", config.wifiname
    ], check=True)