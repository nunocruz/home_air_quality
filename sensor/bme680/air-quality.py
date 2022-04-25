#!/usr/bin/env python

import math
import time
import board
import digitalio
import adafruit_bme680
import weather

#setup
spi = board.SPI()
cs = digitalio.DigitalInOut(board.CE1)
bme680 = adafruit_bme680.Adafruit_BME680_SPI(spi, cs, refresh_rate = 10)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = weather.get_pressure()

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -3

print("""Estimate indoor air quality

Runs the sensor for a burn-in period, then uses a 
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.

Press Ctrl+C to exit

""")

# These oversampling settings can be tweaked to 
# change the balance between accuracy and noise in
# the data.

bme680.humidity_oversample = 2
bme680.pressure_oversample = 4
bme680.temperature_oversample = 4
bme680.filter_size = 3

def dew_point(celsius, humidity):
    a = 17.271
    b = 237.3
    temp = (a * celsius) / (b + celsius) + math.log(humidity / 100)
    return (b * temp) / (a - temp)

# start_time and curr_time ensure that the 
# burn_in_time (in seconds) is kept track of.
start_time = time.time()
curr_time = time.time()
burn_in_time = 300  # burn_in_time (in seconds) is kept track of.

burn_in_data = []

try:
    # Collect gas resistance burn-in values, then use the average
    # of the last 50 values to set the upper limit for calculating
    # gas_baseline.
    print("Collecting gas resistance burn-in data for 5 mins\n")
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        gas = bme680.gas
        burn_in_data.append(gas)
        print("Gas: {0} Ohms".format(gas))
        time.sleep(1)

    gas_baseline = sum(burn_in_data[-50:]) / 50.0

    # Set the humidity baseline to 40%, an optimal indoor humidity.
    hum_baseline = 40.0

    # This sets the balance between humidity and gas reading in the 
    # calculation of air_quality_score (25:75, humidity:gas)
    hum_weighting = 0.25

    print("Gas baseline: {0} Ohms, humidity baseline: {1:.2f} %RH\n".format(gas_baseline, hum_baseline))

    while True:
        gas = bme680.gas
        gas_offset = gas_baseline - gas

        relative_humidity = bme680.relative_humidity
        hum_offset = relative_humidity - hum_baseline

        # Calculate hum_score as the distance from the hum_baseline.
        if hum_offset > 0:
            hum_score = (100 - hum_baseline - hum_offset) / (100 - hum_baseline) * (hum_weighting * 100)

        else:
            hum_score = (hum_baseline + hum_offset) / hum_baseline * (hum_weighting * 100)

        # Calculate gas_score as the distance from the gas_baseline.
        if gas_offset > 0:
            gas_score = (gas / gas_baseline) * (100 - (hum_weighting * 100))

        else:
            gas_score = 100 - (hum_weighting * 100)

        # Calculate air_quality_score. 
        air_quality_score = hum_score + gas_score
        temp = bme680.temperature + temperature_offset
        
        humidity = str(round(relative_humidity, 2))
        temperature = str(round(temp, 2))
        dew = str(round(dew_point(temp,  relative_humidity), 2))
        pressure = str(round(bme680.pressure, 2))
        air_qual = str(round(air_quality_score, 2))
        altitude = str(round(bme680.altitude, 2))

        print("\nTemperature: %s C" % temperature)
        print("Humidity: %s %%" % humidity)
        print("Pressure: %s hPa" % pressure)
        print("Dew Point: %s C" % dew)
        print("Altitude = %s meters" % altitude)
        print("Gas: %d ohm" % gas)
        print("Air quality: %s" % air_qual)

        time.sleep(1)

except KeyboardInterrupt:
    pass
