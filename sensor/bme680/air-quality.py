#!/usr/bin/env python

import config
import math
import sensor
import time

print("""Estimate indoor air quality

Runs the sensor for a burn-in period, then uses a 
combination of relative humidity and gas resistance
to estimate indoor air quality as a percentage.

Press Ctrl+C to exit

""")

bme680 = sensor.bme680

# Collect gas resistance burn-in values, then use the average
# of the last 50 values to set the upper limit for calculating
# gas_baseline.
def gas_baseline(burn_in_time):
    start_time = time.time()
    curr_time = time.time()
    burn_in_data = []
    print("Collecting gas resistance burn-in data for %d seconds\n" % burn_in_time)
    while curr_time - start_time < burn_in_time:
        curr_time = time.time()
        gas = bme680.gas
        burn_in_data.append(gas)
        print("Gas: {0} Ohms".format(gas))
        time.sleep(1)
    return burn_in_data

try:
    burn_in_data = gas_baseline(300);
    gas_baseline = sum(burn_in_data[-50:]) / 50.0
    hum_baseline = config.hum_baseline
    hum_weighting = config.hum_weighting

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
        temp = bme680.temperature + config.temperature_offset
        
        print("\nTemperature: %s C" % str(round(temp, 2)))
        print("Humidity: %s %%" % str(round(relative_humidity, 2)))
        print("Pressure: %s hPa" % str(round(bme680.pressure, 2)))
        print("Dew Point: %s C" % str(round(weather.dew_point(temp,  relative_humidity), 2)))
        print("Altitude = %s meters" % str(round(bme680.altitude, 2)))
        print("Gas: %d ohm" % gas)
        print("Air quality: %s" % str(round(air_quality_score, 2)))

        time.sleep(1)

except KeyboardInterrupt:
    pass
