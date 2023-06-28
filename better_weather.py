import requests
import json
import datetime
import pandas as pd
import sqlalchemy as db

key = "?key=3c978d81b1e84cfc836183128232706"
url = "https://api.weatherapi.com/v1/"
time = "current.json"
url_key = url + time + key
current_date = datetime.datetime.now()

# cols = ["weather", "temp", "wind", "moon"]
data_this_week = pd.DataFrame() # creates empty DataFrame
data_2 = pd.DataFrame()
#{location, current, forecast[forecastday[day, astro, hour]]}
data_location = pd.DataFrame()
data_current = pd.DataFrame()
data_forecast = pd.DataFrame()
data_forecast_day = pd.DataFrame()
data_astro = pd.DataFrame()
data_hour = pd.DataFrame()

response = requests.get("https://api.weatherapi.com/v1/forecast.json?key=3c978d81b1e84cfc836183128232706&q=11234&days=2&hour=12")
week_forecast = response.json()

print(json.dumps(response.json(), indent=3))

# json_normalize - standardizes everything (flattens json into DataFrame)
# DataFrame.from_dict - take everything from the dictionary and makes it into the dataframe 
data_this_week = pd.json_normalize(week_forecast['forecast']['forecastday'][0]['day']) 
data_2 = pd.json_normalize(week_forecast['forecast']['forecastday'][1]['day'])

data_location = pd.json_normalize(week_forecast['location']) 
data_current = pd.json_normalize(week_forecast['current']) 
data_forecast = pd.json_normalize(week_forecast['forecast']) 
data_forecast_day = pd.json_normalize(week_forecast['forecast']['forecastday'][0]['day']) 
data_astro = pd.json_normalize(week_forecast['forecast']['forecastday'][0]['astro']) 
data_hour = pd.json_normalize(week_forecast['forecast']['forecastday'][0]['hour']) 
data_forecast_day2 = pd.json_normalize(week_forecast['forecast']['forecastday'][1]['day'])
data_astro2 = pd.json_normalize(week_forecast['forecast']['forecastday'][1]['astro']) 
data_hour2 = pd.json_normalize(week_forecast['forecast']['forecastday'][1]['hour']) 
# apply - applys fucntion to one column
# applymap - allows you to apply a function to several columns
data_this_week = data_this_week.applymap(json.dumps)
data_location = data_location.applymap(json.dumps)
data_current = data_current.applymap(json.dumps)
data_forecast = data_forecast.applymap(json.dumps)
data_forecast_day = data_forecast_day.applymap(json.dumps)
data_astro = data_astro.applymap(json.dumps)
data_hour = data_hour.applymap(json.dumps)
# data_forecast_day2 = data_forecast_day2.applymap(json.dumps)
# data_astro2 = data_astro2.applymap(json.dumps)
# data_hour2 = data_hour2.applymap(json.dumps)

# creat_engine - creates an engine; need kind of sql and name of database; enginee needs to be connected to database
engine = db.create_engine('sqlite:///thisWeek.db')
# to_sql = converts database to sql
# data_this_week.to_sql('thisWeek', con=engine, if_exists='replace', index=False)

data_location.to_sql('thisWeek', con=engine, if_exists='replace', index=False)
data_current.to_sql('curr', con=engine, if_exists='replace', index=False)
data_forecast.to_sql('cast', con=engine, if_exists='replace', index=False)
data_forecast_day.to_sql('day', con=engine, if_exists='replace', index=False)
data_astro.to_sql('astro', con=engine, if_exists='replace', index=False)
data_hour.to_sql('hour', con=engine, if_exists='replace', index=False)
data_forecast_day2.to_sql('day2', con=engine, if_exists='replace', index=False)
data_astro2.to_sql('astro2', con=engine, if_exists='replace', index=False)
data_hour2.to_sql('hour2', con=engine, if_exists='replace', index=False)


# data_this_week = data_this_week.append(data_2, ignore_index=True)
# connects engine to database
with engine.connect() as connection:
   query_result = connection.execute(db.text("SELECT * FROM thisWeek;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE1")
   query_result = connection.execute(db.text("SELECT * FROM curr;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE2")
   query_result = connection.execute(db.text("SELECT * FROM cast;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE3")
   query_result = connection.execute(db.text("SELECT * FROM day;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE4")
   query_result = connection.execute(db.text("SELECT sunrise FROM astro;")).fetchall()
   print(pd.DataFrame(query_result))
   query_result = connection.execute(db.text("SELECT sunset, moonrise FROM astro;")).fetchall()
   print(pd.DataFrame(query_result).iloc[0,0])
   print("DONE5")
   query_result = connection.execute(db.text("SELECT * FROM hour;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE6")
   query_result = connection.execute(db.text("SELECT * FROM day2;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE4")
   query_result = connection.execute(db.text("SELECT sunrise FROM astro2;")).fetchall()
   print(pd.DataFrame(query_result))
   query_result = connection.execute(db.text("SELECT sunset, moonrise FROM astro2;")).fetchall()
   print(pd.DataFrame(query_result).iloc[0,0])
   print(pd.DataFrame(query_result).iloc[0,1])
   print("DONE5")
   query_result = connection.execute(db.text("SELECT * FROM hour2;")).fetchall()
   print(pd.DataFrame(query_result))
   print("DONE6")

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


# main()
