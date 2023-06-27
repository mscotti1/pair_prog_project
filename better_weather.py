import requests
import json



key = "3c978d81b1e84cfc836183128232706"
zipcode = input("Enter your zipcode:")
url = "https://api.weatherapi.com/v1/future.json?key=" + key + "&q=" + zipcode + "&dt=2023-07-28"


response = requests.get(url)


print(json.dumps(response.json(),indent=3))



