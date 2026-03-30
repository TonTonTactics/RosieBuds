import time
import network
import machine
import dht20
import urequests as requests
import ujson
from machine import Pin, I2C

networkssid = "The_Hub"
networkkey = "12345678"

huburl = 'http://192.168.4.1:8000/sensors/'

i2c = machine.I2C(scl=Pin(26), sda=Pin(33), freq=50000)
dhtsensor = dht20.DHT20(56, i2c)

moisture = machine.ADC (Pin(34))
onepercentmoisture = 35

head = {'Content-Type': 'application/json'}

pinetwork = network.WLAN(network.WLAN.IF_STA) # Might have to use .active() if the object doesn't start activated?
pinetwork.active (False)
time.sleep(5)
pinetwork.active (True)

while True:
    if not pinetwork.isconnected():
        while not pinetwork.isconnected():
            pinetwork.disconnect()
            time.sleep (4)
            print ("Attempting to connect...")
            pinetwork.connect (networkssid, networkkey)
            print (pinetwork.status ())
            time.sleep(4)

        print ("Connected to access point.")
    rawmoisture = moisture.read()
    soilmoisture = (100 - (rawmoisture / onepercentmoisture)) / 100
    
    print (rawmoisture)
    print (i2c.scan())      
    readings = dhtsensor.measurements
    readings.update ({'moisture': soilmoisture})
    readings.update ({'sensor_id': '1'})
    print (readings)

    jsontest = ujson.dumps (readings)
    
    try:
        requests.post(huburl, json=readings)
    except:
        continue
        

    time.sleep(5)
    # machine.deepsleep (600000) # sleep for 10 mins
