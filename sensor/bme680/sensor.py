import adafruit_bme680
import board
import digitalio

#setup
spi = board.SPI()
cs = digitalio.DigitalInOut(board.CE1)
bme680 = adafruit_bme680.Adafruit_BME680_SPI(spi, cs, refresh_rate = 10)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = weather.get_pressure()

# These oversampling settings can be tweaked to 
# change the balance between accuracy and noise in
# the data.
bme680.humidity_oversample = 2
bme680.pressure_oversample = 4
bme680.temperature_oversample = 4
bme680.filter_size = 3