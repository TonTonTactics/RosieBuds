""" 

Yusuf Eldarieby, McMaster, 2026"""

import os

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

makrobo_ds18b20 = "28-00000036660d"

def makerobo_setup():
    global makerobo_ds18b20
    
    for i in os.listdir("/sys/bus/w1/devices"):
        if i != "w1_bus_master1":
            makerobo_ds18b20 = i
            
def makerobo_read():
    makerobo_location = "/sys/bus/w1/devices/" + makerobo_ds18b20 + "/w1_slave"
    makerobo_tfile = open(makerobo_location)
    makerobo_text = makerobo_tfile.read()
    makerobo_tfile.close()
    try:
        secondline = makerobo_text.split("\n")[1]
    except IndexError as e:
        return 0
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return temperature

def makerobo_loop():
    while True:
        if makerobo_read() != None:
            print ("Current temperature : %0.3f C" % makerobo_read())
            
def destroy():
    pass

if __name__ == "__main__":
    try:
        makerobo_setup()
        makerobo_loop()
    except KeyboardInterrupt:
        destroy()
