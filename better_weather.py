import requests
import json
import datetime
import pandas as pd
import sqlalchemy as db
from weather_conditions import ascii_art_dict

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

def database_astro(zipcode, date, porf):
    pass

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
    cols = [" "]
    print("testing table print")
    test = str(pd.DataFrame(data_astro, headers))
    starts = test.find('0') +1
    print(test[starts:])
    print("test done")

    data_location.to_sql('location', con=engine, if_exists='replace', index=False)
    data_forecast_day.to_sql('day', con=engine, if_exists='replace', index=False)
    # data_astro.to_sql('astro', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT name, region, country, lat, lon, localtime FROM location;")).fetchall()
        print(pd.DataFrame(query_result))
        print("Done1")
        query_result = connection.execute(db.text("SELECT * FROM day;")).fetchall()
        print(pd.DataFrame(query_result).iloc[0,14])
        query_result = connection.execute(db.text("SELECT maxtemp_f, mintemp_f, avgtemp_f, maxwind_mph, totalprecip_in, avgvis_miles, avghumidity, uv FROM day;")).fetchall()
        print(pd.DataFrame(query_result))
        print("Done2")
        # query_result = connection.execute(db.text("SELECT * FROM astro;")).fetchall()
        # print(pd.DataFrame(query_result))
        # print("Done3")

    data_hour = pd.DataFrame()
    # data_hour = pd.json_normalize(data_porf['forecast']['forecastday'][0]['hour'][0]) 
    # data_hour = data_hour.applymap(json.dumps)
    # data_hour.to_sql('hour100', con=engine, if_exists='replace', index=False)
    # with engine.connect() as connection:
    #     query_result = connection.execute(db.text("SELECT * FROM hour100;")).fetchall()
    #     for i in range(50):                
    #         print(pd.DataFrame(query_result).iloc[0,])
    if porf == 1:
        for i in range(0,24,3):
            data_hour = pd.json_normalize(data_porf['forecast']['forecastday'][0]['hour'][i]) 
            data_hour = data_hour.applymap(json.dumps)
            data_hour.to_sql('hour' + str(i), con=engine, if_exists='replace', index=False)
            with engine.connect() as connection:
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(i) + ";")).fetchall()             
                print(pd.DataFrame(query_result).iloc[0,32])
                query_result = connection.execute(db.text("SELECT time, temp_f, is_day, uv, wind_mph, wind_degree, wind_dir, precip_in, humidity, cloud, feelslike_f, windchill_f, will_it_rain, will_it_snow, vis_miles FROM hour" + str(i) + ";")).fetchall()
                print(pd.DataFrame(query_result))
                print("Done HOUR: ", i)
    elif porf == 2:
        for i in range(0,8):
            data_hour = pd.json_normalize(data_porf['forecast']['forecastday'][0]['hour'][i]) 
            data_hour = data_hour.applymap(json.dumps)
            data_hour.to_sql('hour' + str(i), con=engine, if_exists='replace', index=False)
            with engine.connect() as connection:
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(i) + ";")).fetchall()             
                print(pd.DataFrame(query_result).iloc[0,32])
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(i) + ";")).fetchall()
                print(pd.DataFrame(query_result))
                print("Done HOUR: ", i)

# database_porf(zipcode, datep, 1)

def database_creater(zipcode, time_range):
    # makes databases for current forecast (time range from 0-14 days) 
    # does not have hour intervals but could add them if necessdary (right now chooses one hour of the day)
    data_location = pd.DataFrame() # creates empty DataFrame
    data_current = pd.DataFrame()
    data_forecast = pd.DataFrame()
    data_forecast_day = pd.DataFrame()
    data_astro = pd.DataFrame()
    data_hour = pd.DataFrame()

    url_database = "https://api.weatherapi.com/v1/forecast.json?key=3c978d81b1e84cfc836183128232706"
    url_database += "&q=" + str(zipcode) + "&days=" + str(time_range)

    response = requests.get(url_database)
    week_forecast = response.json()
    # print(json.dumps(response.json(), indent=3))
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
    data_location.to_sql('location', con=engine, if_exists='replace', index=False)
    data_current.to_sql('curr', con=engine, if_exists='replace', index=False)
    for i in range(time_range):
        data_forecast_day = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['day']) 
        data_astro = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['astro']) 
        data_forecast_day = data_forecast_day.applymap(json.dumps)
        data_astro = data_astro.applymap(json.dumps)
        data_forecast_day.to_sql('day' + str(i), con=engine, if_exists='replace', index=False)
        data_astro.to_sql('astro' + str(i), con=engine, if_exists='replace', index=False)
        for j in range(0,24,3):
            data_hour = pd.json_normalize(week_forecast['forecast']['forecastday'][i]['hour'][j]) 
            data_hour = data_hour.applymap(json.dumps)
            data_hour.to_sql('hour' + str(i) + "_" + str(j), con=engine, if_exists='replace', index=False)

    # connects engine to database
    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT name, region, country, lat, lon, localtime FROM location;")).fetchall()
        print(pd.DataFrame(query_result))
        print("DONE1")
        query_result = connection.execute(db.text("SELECT * FROM curr;")).fetchall()
        print(pd.DataFrame(query_result).iloc[0,22])
        query_result = connection.execute(db.text("SELECT last_updated, temp_f, is_day, uv, wind_mph, wind_degree, wind_dir, gust_mph, precip_in, humidity, cloud, feelslike_f, vis_miles FROM curr;")).fetchall()
        print(pd.DataFrame(query_result))
        print("DONE2")
        for m in range(time_range):
            query_result = connection.execute(db.text("SELECT * FROM day" + str(m) + ";")).fetchall()
            print(pd.DataFrame(query_result).iloc[0,14])
            query_result = connection.execute(db.text("SELECT maxtemp_f, mintemp_f, avgtemp_f, maxwind_mph, totalprecip_in, avgvis_miles, avghumidity, uv FROM day" + str(m) + ";")).fetchall()
            print(pd.DataFrame(query_result))
            print("DONE_", m)
            # query_result = connection.execute(db.text("SELECT * FROM astro" + str(j) + ";")).fetchall()
            # print(pd.DataFrame(query_result))
            # query_result = connection.execute(db.text("SELECT sunset, moonrise FROM astro" + str(j) + ";")).fetchall()
            # print(pd.DataFrame(query_result))
            # print("DONE_", j)
            for n in range(0,24,3):
                query_result = connection.execute(db.text("SELECT * FROM hour" + str(m) + "_" + str(n) + ";")).fetchall()             
                print(pd.DataFrame(query_result).iloc[0,32])
                query_result = connection.execute(db.text("SELECT time, temp_f, is_day, uv, wind_mph, wind_degree, wind_dir, precip_in, humidity, cloud, feelslike_f, windchill_f, will_it_rain, will_it_snow, vis_miles FROM hour" + str(m) + "_" + str(n) + ";")).fetchall()
                print(pd.DataFrame(query_result))
                print("Done HOUR: ", n)
# database_creater(11234, 3)

def weather_getter(zip):
    url = url_key + "&q=" + zip
    response = requests.get(url)
    print(json.dumps(response.json(), indent=3))
    # add alerts
    # try to get date from data


def get_date_str(date):
    # This function returns string of date formatted YYYY-MM-DD
    return str(date)[0:10]


def get_decision(date):
    # This method returns the decision by the user
    # FIX-ME: Should it loop until valid input?
    print("Pleese select one of the following options:")
    str_date = get_date_str(date)
    print(f"1) Get more data on {str_date}")
    print("2) Choose a different date")
    print("3) Leave the program")
    # FIX-ME: Invalid input: '' or longer than 1 character or not 1,2, or 3
    decision = input("Enter the number of your choice: ")
    print()
    return int(decision)


def more_data():
    options = ["Alerts", "Astronomy", "Air quality"]
    print("Pleese select one of the following options:")
    for i, option in enumerate(options):
        print(f'{i+1}) {option}')
    # FIX-ME: Invalid input: '' or longer than 1 character or not 1,2, or 3
    decision = input("Enter 2: ")
    print()
    # to-do 


def get_new_date():
    # TO-DO: FIXE FOR INVALID INPUT
    print("You can enter a date in the past or future")
    date_input = input("Enter a date (YYYY-MM-DD): ")
    date_components = date_input.split('-')

    year = int(date_components[0])
    month = int(date_components[1])
    day = int(date_components[2])

    new_date_obj = datetime.datetime(year, month, day)
    porf = 1 if current_date > new_date_obj else 2
    return new_date_obj, porf


def leave_program_message():
    print(ascii_art_dict['bigSun'])
    print("Hope you stay chill'n")

def main():

    print("\nWelcome to Better Weather!!!\n")
    zipcode = input("Please enter your zipcode: ")
    print()
    date = current_date
    porf = 0

    # TO-DO: format output text with data wanted to display
    database_creater(zipcode,1)

    while True:

        # FIX-ME: format for question?
        decision = get_decision(date)

        # TO-DO: either make a function for each decision or make functionality
        if decision == 1:
            more_data()
        elif decision == 2:
            new_date,porf = get_new_date()
            date = new_date
            print(date,'\n')
            database_porf(zipcode, date, porf)
        elif decision == 3:
            leave_program_message()
            break            
        else:
            pass

main()