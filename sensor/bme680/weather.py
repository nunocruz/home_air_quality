import requests
import json

#https://api.openweathermap.org/data/2.5/onecall?lat=52.369670&lon=4.882320&exclude=minutely,hourly,daily,alerts&units=metric&appid=

base_url = "https://api.openweathermap.org/data/2.5/onecall"
params = dict()
params["lat"] = "52.369670"
params["lon"] = "4.882320"
params["exclude"] = "minutely,hourly,daily,alerts"
params["units"] = "metric"
params["appid"] = "631da37fe3eef2ae16ec89d22d7f38ea"


def get_current_weather():
	url = requests.get(base_url, params=params)
	data = json.loads(url.text)
	return data['current']

def get_pressure():
	current_weather = get_current_weather()
	return current_weather['pressure']
