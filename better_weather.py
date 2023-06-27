import requests
import json
## importing socket module
import socket
## getting the hostname by socket.gethostname() method
hostname = socket.gethostname()
## getting the IP address using socket.gethostbyname() method
ip_address = socket.gethostbyname(hostname)
## printing the hostname and ip_address
print(f"Hostname: {hostname}")
print(f"IP Address: {ip_address}")

url = "https://api.weather.gov/"
ex_forecast = "points/40.678177,-73.944160"
ex_forecast = "points/42.0345,-93.6203"

ex_alerts = "alerts/active?area=KS"
response = requests.get(url+ex_forecast)
# response = requests.get(url+ex_alerts)
print(response)
print(json.dumps(response.json(), indent=3))

