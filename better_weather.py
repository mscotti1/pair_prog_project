import requests
import json
import datetime
import pandas as pd
import sqlalchemy as db

# [sunny, partly cloudy, cloudy, raining, snowing, thunderstorm, blizard?, hurricane?, tsunami?, tornado?, typhoon?, drought?, earthquake?]
key = "?key=3c978d81b1e84cfc836183128232706"
url = "https://api.weatherapi.com/v1/"
time = "current.json"
url_key = url + time + key
current_date = datetime.datetime.now()
zipcode = 11234
time_range = 3
hours = 12
datep = "2023-06-01"
datef = "2023-07-25"

# future automatically does 3 hour intervals but history does every hour so I made history do 3 hour intervals as well just to match

def database_porf(zipcode, date, porf):
    # makes database for past or future date and uses 3 hour intervals
    p = "history.json"
    f = "future.json"
    if porf == 1:
        url_database = "https://api.weatherapi.com/v1/" + p + "?key=3c978d81b1e84cfc836183128232706"
    elif porf == 2:
        url_database = "https://api.weatherapi.com/v1/" + f + "?key=3c978d81b1e84cfc836183128232706"
    
    url_database += "&q=" + str(zipcode) + "&dt=" + date
    response = requests.get(url_database)
    data_porf= response.json()
    # print(json.dumps(response.json(), indent=3))
    engine = db.create_engine('sqlite:///history.db')

    data_location = pd.DataFrame()
    data_forecast_day = pd.DataFrame()
    data_astro = pd.DataFrame()

    data_location = pd.json_normalize(data_porf['location'])
    data_forecast_day = pd.json_normalize(data_porf['forecast']['forecastday'][0]['day']) 
    data_astro = pd.json_normalize(data_porf['forecast']['forecastday'][0]['astro']) 

    data_location = data_location.applymap(json.dumps)
    data_forecast_day = data_forecast_day.applymap(json.dumps)
    data_astro = data_astro.applymap(json.dumps)
    data_astro = [data_astro[i] for i in data_astro]
    print(data_astro)

    headers = ['sunrise', 'sunset', 'moonrise', 'moonset', 'moonphase', 'moonillumination']
    print("testing table print")
    print(print(pd.DataFrame(data_astro, headers)))
    print("test done")

    data_location.to_sql('location', con=engine, if_exists='replace', index=False)
    data_forecast_day.to_sql('day', con=engine, if_exists='replace', index=False)
    # data_astro.to_sql('astro', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM location;")).fetchall()
        print(pd.DataFrame(query_result))
        print("Done1")
        query_result = connection.execute(db.text("SELECT * FROM day;")).fetchall()
        print(pd.DataFrame(query_result))
        print("Done2")
        # query_result = connection.execute(db.text("SELECT * FROM astro;")).fetchall()
        # print(pd.DataFrame(query_result))
        # print("Done3")

    data_hour = pd.DataFrame()
    if porf == 1:
        for i in range(0,24,3):
            data_hour = pd.json_normalize(data_porf['forecast']['forecastday'][0]['hour'][i]) 
            data_hour = data_hour.applymap(json.dumps)
            data_hour.to_sql('hour' + str(i), con=engine, if_exists='replace', index=False)
            with engine.connect() as connection:
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(i) + ";")).fetchall()
                print(pd.DataFrame(query_result))
                print("Done HOUR: ", i)
    elif porf == 2:
        for i in range(0,8):
            data_hour = pd.json_normalize(data_porf['forecast']['forecastday'][0]['hour'][i]) 
            data_hour = data_hour.applymap(json.dumps)
            data_hour.to_sql('hour' + str(i), con=engine, if_exists='replace', index=False)
            with engine.connect() as connection:
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(i) + ";")).fetchall()
                print(pd.DataFrame(query_result))
                print("Done HOUR: ", i)

database_porf(zipcode, datep, 1)

def database_creater(zipcode, time_range, hour):
    # makes databases for current forecast (time range from 0-14 days) 
    # does not have hour intervals but could add them if necessdary (right now chooses one hour of the day)
    data_location = pd.DataFrame() # creates empty DataFrame
    data_current = pd.DataFrame()
    data_forecast = pd.DataFrame()
    data_forecast_day = pd.DataFrame()
    data_astro = pd.DataFrame()
    data_hour = pd.DataFrame()

    url_database = "https://api.weatherapi.com/v1/forecast.json?key=3c978d81b1e84cfc836183128232706"
    url_database += "&q=" + str(zipcode) + "&days=" + str(time_range) + "&hour=" + str(hour)

    response = requests.get(url_database)
    week_forecast = response.json()
    print(json.dumps(response.json(), indent=3))
    # creat_engine - creates an engine; need kind of sql and name of database; enginee needs to be connected to database
    engine = db.create_engine('sqlite:///thisWeek.db')

    # json_normalize - standardizes everything (flattens json into DataFrame)
    # DataFrame.from_dict - take everything from the dictionary and makes it into the dataframe 
    data_location = pd.json_normalize(week_forecast['location']) 
    data_current = pd.json_normalize(week_forecast['current']) 
    # apply - applys fucntion to one column
    # applymap - allows you to apply a function to several columns
    data_location = data_location.applymap(json.dumps)
    data_current = data_current.applymap(json.dumps)
    # to_sql = converts database to sql
    data_location.to_sql('thisWeek', con=engine, if_exists='replace', index=False)
    data_current.to_sql('curr', con=engine, if_exists='replace', index=False)
    for i in range(time_range):
        data_forecast_day = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['day']) 
        data_astro = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['astro']) 
        data_hour = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['hour']) 
        data_forecast_day = data_forecast_day.applymap(json.dumps)
        data_astro = data_astro.applymap(json.dumps)
        data_hour = data_hour.applymap(json.dumps)
        data_forecast_day.to_sql('day' + str(i), con=engine, if_exists='replace', index=False)
        data_astro.to_sql('astro' + str(i), con=engine, if_exists='replace', index=False)
        data_hour.to_sql('hour' + str(i), con=engine, if_exists='replace', index=False)

    # connects engine to database
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM thisWeek;")).fetchall()
        print(pd.DataFrame(query_result))
        print("DONE1")
        query_result = connection.execute(db.text("SELECT * FROM curr;")).fetchall()
        print(pd.DataFrame(query_result))
        print("DONE2")
        for j in range(time_range):
            query_result = connection.execute(db.text("SELECT * FROM day" + str(j) + ";")).fetchall()
            print(pd.DataFrame(query_result))
            print("DONE_", j)
            query_result = connection.execute(db.text("SELECT * FROM astro" + str(j) + ";")).fetchall()
            print(pd.DataFrame(query_result))
            query_result = connection.execute(db.text("SELECT sunset, moonrise FROM astro" + str(j) + ";")).fetchall()
            print(pd.DataFrame(query_result))
            # print(pd.DataFrame(query_result).iloc[0,0])
            # print(pd.DataFrame(query_result).iloc[0,1])
            print("DONE_", j)
            query_result = connection.execute(db.text("SELECT * FROM hour" + str(j) + ";")).fetchall()
            print(pd.DataFrame(query_result))
            print("DONE_", j)

# database_creater(11234, 3, 12)

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
        porf = int(input("Please input the past(1), future(2), or neither(0): "))
    
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


# main()
