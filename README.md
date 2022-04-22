# home_air_quality
Using a BME680 from Adadruit and a raspberry Pi to create an airquality dashboard. 

# Instalation

## CircuitPython
```
cd ~
sudo pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo python3 raspi-blinka.py
```
More at: https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

## BME680 library
```
sudo pip3 install adafruit-circuitpython-bme680
```
More at: https://learn.adafruit.com/adafruit-bme680-humidity-temperature-barometic-pressure-voc-gas/python-circuitpython

Documentation at: https://docs.circuitpython.org/projects/bme680/en/latest/