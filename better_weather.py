import requests
import json
import datetime

key = "?key=3c978d81b1e84cfc836183128232706"
url = "https://api.weatherapi.com/v1/"
time = "current.json"
url_key = url + time + key
current_date = datetime.datetime.now()

def weather_getter(zip):
    url =  url_key + "&q=" + zip
    response = requests.get(url)
    print(json.dumps(response.json(),indent=3))
    # add alerts
    # try to get date from data

# This function returns the date n days forward or backwards
def get_new_date(num):
     new_date = datetime.datetime.now()
     new_date += datetime.timedelta(days=num)
     return new_date

# This function returns string of date formatted YYYY-MM-DD
def get_date_str(date):
    return str(date)[0:10]

def main():

    # Uses get_date_str to print date formatted YYYY-MM-DD
    # current_date is a global variable for current date
    print(get_date_str(current_date))

    # Place holder for new date
    new_date = get_new_date(4)
    # print out future date using get_date_str
    print(get_date_str(new_date))

    zipcode = input("Enter your zipcode: ")
    weather_getter(zipcode)
    # Print out current forecast and then ask if they want anymore data from future or past days
    # History has to be on or after Jan 1st 2010
    # Future has to be at leat 14 days into the future
    time_range = input("How many days in the future (at least 14)? ")
    new_date = get_new_date(int(time_range))
    str_nd = get_date_str(new_date)
    
    url = "https://api.weatherapi.com/v1/future.json" + key + "&q=" + zipcode + "&dt=" + str_nd


    response = requests.get(url)
    print(json.dumps(response.json(),indent=3))

main()


