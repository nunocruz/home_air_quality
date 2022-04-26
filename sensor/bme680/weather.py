import requests
import json
import config

base_url = "https://api.openweathermap.org/data/2.5/onecall"
params = dict()
params["lat"] = config.latitude
params["lon"] = config.longitude
params["exclude"] = "minutely,hourly,daily,alerts"
params["units"] = "metric"
params["appid"] = config.api_key


def get_current_weather():
	url = requests.get(base_url, params=params)
	data = json.loads(url.text)
	return data['current']

def get_pressure():
	current_weather = get_current_weather()
	return current_weather['pressure']

def dew_point(celsius, humidity):
    a = 17.271
    b = 237.3
    temp = (a * celsius) / (b + celsius) + math.log(humidity / 100)
    return (b * temp) / (a - temp)

#print(get_pressure())