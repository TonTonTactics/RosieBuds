import time
import network
import requests
import machine
import dht20

# from dht20_sensor import sensor

networkssid = "monday-46"
networkkey = "raspberry"
# Web database location = http://127.0.0.1:8000/sensors/

# Soil moisture range [0-2500]

'''networkssid = "Gabriel's Pixel"
networkkey = "abcd1234"'''

huburl = 'https://192.168.4.1/sensors/'

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
