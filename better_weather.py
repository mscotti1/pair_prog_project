import requests
import json

key = "?key=3c978d81b1e84cfc836183128232706"
url = "https://api.weatherapi.com/v1/"
time = "current.json"
url_key = url + time + key

def weather_getter(zip):
    url =  url_key + "&q=" + zip
    response = requests.get(url)
    print(json.dumps(response.json(),indent=3))
    # add alerts
    # try to get date from data


def main():
    zipcode = input("Enter your zipcode: ")
    weather_getter(zipcode)
    # Print out current forecast and then ask if they want anymore data from future or past days
    # History has to be on or after Jan 1st 2010
    # Future has to be at leat 14 days into the future
    time_range = input("How many days in the future (at least 14)? ")
   
    url = "https://api.weatherapi.com/v1/future.json?key=" + key + "&q=" + zipcode + "&dt=2023-07-11"


    response = requests.get(url)
    print(json.dumps(response.json(),indent=3))

main()


