import requests
import json

#https://api.openweathermap.org/data/2.5/onecall?lat=***REMOVED***&lon=***REMOVED***&exclude=minutely,hourly,daily,alerts&units=metric&appid=

base_url = "https://api.openweathermap.org/data/2.5/onecall"
params = dict()
params["lat"] = "***REMOVED***"
params["lon"] = "***REMOVED***"
params["exclude"] = "minutely,hourly,daily,alerts"
params["units"] = "metric"
params["appid"] = "***REMOVED***"


def get_current_weather():
	url = requests.get(base_url, params=params)
	data = json.loads(url.text)
	return data['current']

def get_pressure():
	current_weather = get_current_weather()
	return current_weather['pressure']
