'''Gabriel Walker 2026
P3 ESP8266 Wifi Module Code

TODO:
- Setup socket and data sending mechanism'''

import time
import network
import dht
from machine import Pin

networkssid = "ENTER SSID"
networkkey = "ENTER KEY"

dhtsensor = dht.DHT22(Pin(15))

# pinetwork = network.WLAN(network.WLAN.IF_STA) # Might have to use .active() if the object doesn't start activated?

firstloop = True
MAXTEMPVARIANCE = 10
MAXHUMIDVARIANCE = 5
temppredict = 0
tempbuffer = []
tempbuffertracker = 0
tempdeltatracker = 0
tempdeltas = []
BUFFERSIZE = 6

for i in range (0, BUFFERSIZE): # Setting up buffer and delta lists
    tempbuffer.append (0)

for j in range (0, BUFFERSIZE - 1):
    tempdeltas.append (0)

while True:

    if firstloop == True:
        firstloop = False

    else:
        '''if not pinetwork.isconnected():
            while not pinetwork.isconnected():
                pinetwork.connect (networkssid, networkkey)
                print ("Attempting to connect...")
                time.sleep(3000)

            print ("Connected to access point.")'''
        dhtsensor.measure ()
        currentkelvin = dhtsensor.temperature () + 273.15

        tempbuffer [tempbuffertracker] = currentkelvin
        if tempbuffertracker != 0:
            tempdeltas [tempdeltatracker] = tempbuffer [tempbuffertracker] - tempbuffer [tempbuffertracker - 1]
        else:
            tempdeltas [tempdeltatracker] = tempbuffer [tempbuffertracker] - tempbuffer [BUFFERSIZE - 1]
        
        if abs (currentkelvin - temppredict) > MAXTEMPVARIANCE:# Print if temperature is out of range
            print ("Temperature reading outside of limits. Test sensor for incorrect readings.")

        else:
            print (currentkelvin)
        
        # In this section we estimate the next value based on how it has been changing (Mean Value Theorem)
        temppredict = currentkelvin + (sum(tempdeltas) / BUFFERSIZE)
        print (str(tempbuffer))
        print ("Temp predict:\t" + str (temppredict))

        tempbuffertracker += 1
        tempdeltatracker += 1
        print ("Buffer Tracker: " + str (tempbuffertracker))
        print ("Deleta Tracker: " + str (tempdeltatracker))
        if tempbuffertracker >= BUFFERSIZE:
            tempbuffertracker = 0

        if tempdeltatracker >= BUFFERSIZE - 1:
            tempdeltatracker = 0

    time.sleep(2)
