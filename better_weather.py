import requests
import json

url = "https://api.weather.gov/"
ex_forecast = "points/40.678177,-73.944160"
ex_forecast = "points/42.0345,-93.6203"

ex_alerts = "alerts/active?area=KS"
response = requests.get(url+ex_forecast)
# response = requests.get(url+ex_alerts)
print(response)
print(json.dumps(response.json(), indent=3))

