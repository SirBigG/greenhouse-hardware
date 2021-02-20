import time
import json
from urllib import parse, request

import Adafruit_DHT

import spidev

# Setup dht11
sensor = Adafruit_DHT.DHT11
gpio = 4


# Setup soil moisture sensor with analog out data
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000
 
def readChannel(channel):
    val = spi.xfer2([1,(8+channel)<<4,0])
    data = ((val[1]&3) << 8) + val[2]
    return data


if __name__ == "__main__":
    while True:
        h, t = Adafruit_DHT.read_retry(sensor, gpio)
        m = readChannel(0)
        print(h, t, m)
        if h is not None and t is not None and m != 0:
            data = json.dumps({"temperature": t, "humidity": h, "moisture": (m/1023) * 100}).encode()
            req =  request.Request("http://greenhouse-api.agromega.in.ua/store/data", data=data, headers={'Content-Type':'application/json'}) # this will make the method "POST"
            resp = request.urlopen(req)
        time.sleep(10)
