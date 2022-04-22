# SPDX-FileCopyrightText: 2021 Carter Nelson for Adafruit Industries
# SPDX-License-Identifier: MIT

import math
import time
import board
import digitalio
import adafruit_bme680

#data_pulling_interval
interval = 1

#setup
spi = board.SPI()
cs = digitalio.DigitalInOut(board.CE1)
bme680 = adafruit_bme680.Adafruit_BME680_SPI(spi, cs, refresh_rate = interval)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1006.64

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -2

def dew_point(celsius, humidity):
    a = 17.271
    b = 237.3
    temp = (a * celsius) / (b + celsius) + math.log(humidity / 100)
    return (b * temp) / (a - temp)

while True:
    print("\nTemperature: %0.1f C" % (bme680.temperature + temperature_offset))
    print("Humidity: %0.1f %%" % bme680.relative_humidity)
    print("Dew Point: %0.1f C" % dew_point(bme680.temperature + temperature_offset,  bme680.relative_humidity))
    print("Pressure: %0.3f hPa" % bme680.pressure)
    print("Altitude = %0.2f meters" % bme680.altitude)
    print("Gas: %d ohm" % bme680.gas)

    time.sleep(interval)

