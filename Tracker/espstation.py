import time
import network
import machine
import dht20
import urequests as requests
import ujson as json
from machine import Pin, I2C
# from dht20_sensor import sensor

CREDS_FILE = "/hub_credentials.json"

AP_SSID = "The Hub"
AP_PASSWORD = "12345678"

START_URL= "http://192.168.4.1:9000/provision/start"
GET_URL =  "http://192.168.4.1:9000/provision/credentials"

def get_wlan():
    wlan = network.WLAN(network.STA_IF)

    try:
        wlan.disconnect()
    except:
        pass

    wlan.active(False)
    time.sleep(2)
    wlan.active(True)
    time.sleep(2)

    return wlan

def disconnect_wifi(wlan):
    try:
        wlan.disconnect()
    except Exception as e:
        print("Disconnect error:", e)

    try:
        wlan.active(False)
        time.sleep(1)
        wlan.active(True)
        time.sleep(1)
    except Exception as e:
        print("Radio reset error:", e)

def scan_for_ssid(wlan, target_ssid):
    try:
        nets = wlan.scan()
        for net in nets:
            ssid = net[0]
            bssid = net[1]
            channel = net[2]
            rssi = net[3]
            authmode = net[4]
            hidden = net[5]
            
            if isinstance(ssid, bytes):
                ssid = ssid.decode()
            print("SSID", ssid)
            
            if ssid == target_ssid:
                return True
            
    except Exception as e:
        print("Scan error:", e)
    return False

def connect_to_wifi(wlan, ssid, password="", timeout=15):
    disconnect_wifi(wlan)

    print("Connecting to:", ssid)

    try:
        if password:
            wlan.connect(ssid, password)
        else:
            wlan.connect(ssid)
    except Exception as e:
        print("Connect call failed:", e)
        return False

    start = time.time()
    while time.time() - start < timeout:
        if wlan.isconnected():
            print("Connected:", wlan.ifconfig())
            return True
        time.sleep(1)

    print("Connection timeout for:", ssid)
    disconnect_wifi(wlan)
    return False

def wait_for_hub_ap(wlan, target_ssid="The Hub"):
    while True:
        print("Scanning for:", target_ssid)
        found = scan_for_ssid(wlan, target_ssid)

        if found:
            print("Found Hub AP")
            ok = connect_to_wifi(wlan, target_ssid, AP_PASSWORD, timeout=10)
            if ok:
                return True

        print("Hub AP not connected, retrying...")
        time.sleep(3)

def notify_hub_tracker_connected():
    response = None
    try:
        response = requests.post(START_URL, json={"device": "tracker"})
        print("Start status:", response.status_code)
        return response.status_code == 200
    except Exception as e:
        print("Notify hub failed:", e)
        return False
    finally:
        if response is not None:
            response.close()

def get_home_wifi_credentials():
    response = None
    try:
        response = requests.get(GET_URL)
        print("Credentials status:", response.status_code)

        if response.status_code != 200:
            return None

        data = response.json()
        print("Received:", data)

        ssid = data.get("ssid")
        password = data.get("password", "")
        hub_ip = data.get("hub_ip")
        hub_port = data.get("hub_port")

        if not ssid:
            print("No ssid in payload")
            return None

        return {
            "ssid": ssid,
            "password": password,
            "hub_ip": hub_ip,
            "hub_port": hub_port,
        }

    except Exception as e:
        print("Get credentials failed:", e)
        return None
    finally:
        if response is not None:
            response.close()
            

def provision_tracker():
    wlan = get_wlan()

    while True:
        wait_for_hub_ap(wlan, AP_SSID)

        notify_hub_tracker_connected()

        creds = get_home_wifi_credentials()
        if not creds:
            print("No credentials yet. Staying in loop.")
            disconnect_wifi(wlan)
            time.sleep(3)
            continue

        print("Got Credentials:", creds)

        # SAVE NEW CREDS IMMEDIATELY
        save_hub_credentials(
            creds["ssid"],
            creds["password"],
            creds.get("hub_ip"),
            creds.get("hub_port"),
        )
        print("Saved new hub/home credentials locally.")

        print("Waiting before switch to home wifi...")
        disconnect_wifi(wlan)
        time.sleep(10)

        home_ssid = creds["ssid"]
        home_password = creds["password"]

        ok = connect_to_wifi(wlan, home_ssid, home_password, timeout=15)
        if ok:
            print("Provisioning complete")
            return wlan

        print("Home Wi-Fi failed. Retry full process.")
        time.sleep(3)
        
def save_hub_credentials(ssid, password, hub_ip=None, hub_port=None):
    print("SAVING CREDS:", ssid, password)

    data = {
        "ssid": ssid,
        "password": password,
        "hub_ip": hub_ip,
        "hub_port": hub_port,
    }

    with open("/hub_credentials.json", "w") as f:
        json.dump(data, f)

    print("Saved successfully.")
    
def load_hub_credentials():
    try:
        with open(CREDS_FILE, "r") as f:
            return json.load(f)
    except:
        return None
    
def connect_using_saved_credentials():
    creds = load_hub_credentials()

    if not creds:
        print("No saved credentials.")
        return None

    wlan = get_wlan()

    ssid = creds["ssid"]
    password = creds["password"]

    print("Using saved credentials:", ssid)

    ok = connect_to_wifi(wlan, ssid, password, timeout=15)
    if ok:
        print("Connected using saved credentials")
        return wlan

    print("Saved credentials failed.")
    return None
    
def create_sensor_payload(dhtsensor, moisture):
    readings = dhtsensor.measurements
    soil_value = moisture.read()

    return {
        "sensor_id": "tracker-1",
        "moisture": float(soil_value),
        "temperature": float(readings["t"]),
        "humidity": float(readings["rh"]),
    }


def post_sensor_data(payload):
    response = None
    try:
        response = requests.post(SENSOR_POST_URL, json=payload)
        print("POST status:", response.status_code)

        if response.status_code != 200 and response.status_code != 201:
            print("POST failed:", response.text)
            return False

        print("Data sent:", payload)
        return True

    except Exception as e:
        print("Post sensor data failed:", e)
        return False

    finally:
        if response is not None:
            response.close()
        
def main():
    wlan = connect_using_saved_credentials()

    if not wlan:
        print("Falling back to provisioning...")
        wlan = provision_tracker()

    i2c = machine.I2C(scl=Pin(22), sda=Pin(21), freq=50000)
    dhtsensor = dht20.DHT20(56, i2c)
    moisture = machine.ADC(Pin(4))

    while True:
        try:
            if not wlan.isconnected():
                print("Lost Wi-Fi. Reconnecting using saved creds...")
                
                wlan = connect_using_saved_credentials()
                if not wlan:
                    print("Re-provisioning...")
                    wlan = provision_tracker()
                
                continue

            payload = create_sensor_payload(dhtsensor, moisture)
            post_sensor_data(payload)

        except Exception as e:
            print("Main loop error:", e)

        time.sleep(5)


main()


    

"""
networkssid = "monday-46"
networkkey = "raspberry"
# Web database location = http://127.0.0.1:8000/sensors/

# Soil moisture range [0-2500]

'''networkssid = "Gabriel's Pixel"
networkkey = "abcd1234"'''

huburl = 'https://192.168.4.2:8000/sensors/'

i2c = machine.I2C(scl=Pin(22), sda=Pin(21), freq=50000)
dhtsensor = dht20.DHT20(56, i2c)

moisture = machine.ADC (Pin(4))

'''pinetwork = network.WLAN(network.WLAN.IF_STA) # Might have to use .active() if the object doesn't start activated?
pinetwork.active (False)
time.sleep(5)
pinetwork.active (True)'''

while True:
    '''if not pinetwork.isconnected():
        while not pinetwork.isconnected():
            print(pinetwork.scan())
            pinetwork.connect (networkssid)
            print ("Attempting to connect...")
            time.sleep(3)

        print ("Connected to access point.")'''
    soilmoisture = moisture.read()  
    print (soilmoisture)
    print (i2c.scan())      
    readings = dhtsensor.measurements
        
    print (readings)
    
    r = requests.post(huburl, data='Hi')

    time.sleep(2)

"""
