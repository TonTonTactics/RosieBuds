import subprocess


HOTSPOT_NAME = "hub-ap"
HOTSPOT_SSID = "The Hub"
HOTSPOT_PASSWORD = "plantsetup123"


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


def start_ap_mode(
    ssid: str = HOTSPOT_SSID,
    password: str = HOTSPOT_PASSWORD,
    ifname: str = "wlan0"
):
    """Start access point mode with NetworkManager."""
    cmd = [
        "nmcli", "device", "wifi", "hotspot",
        "ifname", ifname,
        "con-name", HOTSPOT_NAME,
        "ssid", ssid,
        "password", password,
    ]
    return run_cmd(cmd)


def stop_ap_mode(ifname: str = "wlan0"):
    """Stop access point mode."""
    # Try bringing down the named hotspot connection first
    result = run_cmd([
        "nmcli", "connection", "down", HOTSPOT_NAME
    ])
    if result["success"]:
        return result

    # Fallback: disconnect the device
    return run_cmd([
        "nmcli", "device", "disconnect", ifname
    ])