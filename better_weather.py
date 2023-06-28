import requests
import json
import datetime

key = "?key=3c978d81b1e84cfc836183128232706"
url = "https://api.weatherapi.com/v1/"
time = "current.json"
url_key = url + time + key
current_date = datetime.datetime.now()


def weather_getter(zip):
    url = url_key + "&q=" + zip
    response = requests.get(url)
    print(json.dumps(response.json(), indent=3))
    # add alerts
    # try to get date from data


def get_new_date(num, porf):
    # This function returns the date n days forward or backwards
    new_date = datetime.datetime.now()
    if porf == 1:
        new_date += datetime.timedelta(days=num)
    elif porf == 2:
        new_date -= datetime.timedelta(days=num)
    return new_date


def get_date_str(date):
    # This function returns string of date formatted YYYY-MM-DD
    return str(date)[0:10]


def main():

    # Uses get_date_str to print date formatted YYYY-MM-DD
    # current_date is a global variable for current date
    print(get_date_str(current_date))
    print(current_date.strftime("%a"))

    # Place holder for new date
    new_date = get_new_date(4,1)
    # print out future date using get_date_str
    print(get_date_str(new_date))

    zipcode = input("Enter your zipcode: ")
    weather_getter(zipcode)
    # Print out current forecast and then ask if they want anymore
    # data from future or past days
    # History has to be on or after Jan 1st 2010
    # Future has to be at leat 14 days into the future
    porf = int(input("Would you like data from the future(1) or the past(2), if neither 0: "))
    if porf == 1:
        time_range = int(input("How many days in the future (at least 14)? "))

        new_date = get_new_date(time_range, porf)
        str_nd = get_date_str(new_date)

        url = "https://api.weatherapi.com/v1/future.json" + \
            key + "&q=" + zipcode + "&dt=" + str_nd
    elif porf == 2:
        time_range = int(input("How many days in the past (no earlier than 2010-01-01)? "))

        new_date = get_new_date(time_range, porf)
        str_nd = get_date_str(new_date)

        url = "https://api.weatherapi.com/v1/history.json" + \
            key + "&q=" + zipcode + "&dt=" + str_nd
    elif porf == 0:
        time_range = 0
    else:
        porf = int(input("Please input future(1), the past(2), or neither(0): "))
    
    # new_date = get_new_date(int(time_range))
    # str_nd = get_date_str(new_date)

    # url = "https://api.weatherapi.com/v1/future.json" + \
    #     key + "&q=" + zipcode + "&dt=" + str_nd

    others = input("Would you like information about the tides, moon cycle, etc? (y or n)")
    if others == 'y':
        print("@Kalem do we want to ask about this and then output stuff? Or are we just parsing the data and printing out everything?")
    if others == 'n':
        print("@Klaem how would you like to incorporate a database? Also would you like to add the option to just put the date in the future or past instead of the days?")

    response = requests.get(url)
    print(json.dumps(response.json(), indent=3))


main()
