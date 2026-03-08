""" 

Yusuf Eldarieby, McMaster, 2026"""

import time
import board
import adafruit_dht

makerobo_dhtDevice = adafruit_dht.DHT22(board.D17, use_pulseio=False)

def loop():
    while True:
        try:
            temperature_c = makerobo_dhtDevice.temperature
            temperature_f = temperature_c * (9/5) + 32
            humidity = makerobo_dhtDevice.humidity
            print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(temperature_f, temperature_c, humidity))
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            makerobo_dhtDevice.exit()
            raise error
        time.sleep(2.0)
        
    
if __name__ == "__main__":
    try:
        while True:
            loop()
    except KeyboardInterrupt:
        pass
