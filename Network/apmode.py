import subprocess

def start_ap_mode(ssid="The Hub"):
    """Start access point mode"""
    try:
        subprocess.run([
            "nmcli","dev","wifi","hotspot",
            "ssid", ssid
        ], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"Error starting AP mode: {e}")

def stop_ap_mode():
    """Stop access point mode"""
    try:
        subprocess.run([
            "nmcli","dev","wifi","hotspot","stop"
        ], check=True)
    
    except subprocess.CalledProcessError as e:
        print(f"Error stopping AP mode: {e}")