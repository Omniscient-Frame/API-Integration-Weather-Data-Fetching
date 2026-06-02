import sqlite3 as sq
import requests
import pandas as pd
import numpy as np
import csv 
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv("API_KEY")

direct_base_url = "http://api.openweathermap.org/geo/1.0/direct?"
# http://api.openweathermap.org/geo/1.0/direct?q=London&limit=5&appid={API key}

coord_base_url = "https://api.openweathermap.org/data/2.5/weather?"
# https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}


def FindCoord(City_Name):
    Name_Based_url = f"{direct_base_url}q={City_Name}&limit=1&appid={API_key}"
    res = requests.get(Name_Based_url)
    info = res.json()
    print("Geo status code : ",res.status_code)
    
    if res.status_code == 200:
        if info == [] :
            print("City not found")
            return None

        coord = info[0]
        latitutude = coord["lat"]
        longitude = coord["lon"]
        print("latitude : ",latitutude)
        print("longitude : ",longitude)
        return [latitutude,longitude]

    else:
        print("Error : ",res.text)
        return None
    

def get_weather_info(coordinate):
    coord_url = f"{coord_base_url}lat={coordinate[0]}&lon={coordinate[1]}&appid={API_key}&units=metric"
    res = requests.get(coord_url)
    if res.status_code !=200:
        print("Error : ",res.text)
        return None
    return res.json()


def WeatherAnalysis(city_name,weather_info):
    return {
    "City Name": city_name,
    "Temp": weather_info["main"]["temp"],
    "Feels_Like": weather_info["main"]["feels_like"],
    "Pressure": weather_info["main"]["pressure"],
    "Humidity": weather_info["main"]["humidity"],
    "Description": weather_info["weather"][0]["description"],
    "Wind_Speed": weather_info["wind"]["speed"],
    "Wind_Deg": weather_info["wind"].get("deg"),
    "Cloudiness": weather_info["clouds"]["all"],
    "Visibility": weather_info["visibility"],
    "Sunrise": weather_info["sys"]["sunrise"],
    "Sunset": weather_info["sys"]["sunset"]
    }

Db_Name = "Weather_Data.db"
Table_name = "Weather"

def PresentInfo():
    City_Name = input("Enter the name of the city: ").strip()
    coordinates = FindCoord(City_Name)

    if coordinates == None:
        print("coordinate not found...exiting")
        print("Enter Valid City Name..")
        return

    weather_info = get_weather_info(coordinates)

    data = pd.DataFrame([WeatherAnalysis(City_Name,weather_info)])    
    data.insert(1,"Date",datetime.now().strftime("%Y-%m-%d"))

    SaveToDb(data)
    print(f"Saved to {Db_Name} in table '{Table_name}'")

    print(data.to_string())
    

def SaveToDb(df):
    conn = sq.connect(Db_Name)
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS weather (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    "City Name" TEXT NOT NULL,
    Date TEXT NOT NULL,
    Temp REAL,
    Feels_Like REAL,
    Pressure REAL,
    Humidity REAL,
    Description TEXT,
    Wind_Speed REAL,
    Wind_Degree REAL,
    Cloudiness INTEGER,
    Visibility INTEGER,
    Sunrise INTEGER,
    Sunset INTEGER,
    UNIQUE("City Name", Date))""")

    row = df.iloc[0].to_dict()
    
    cur.execute("""
    INSERT OR IGNORE INTO weather
    ("City Name", Date, Temp, Feels_Like, Pressure, Humidity, Description,
     Wind_Speed, Wind_Degree, Cloudiness, Visibility, Sunrise, Sunset)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,(row["City Name"], row["Date"], row["Temp"], row["Feels_Like"],
    row["Pressure"], row["Humidity"], row["Description"],
    row["Wind_Speed"], row["Wind_Deg"], row["Cloudiness"],
    row["Visibility"], row["Sunrise"], row["Sunset"]))

    conn.commit()
    conn.close()


def main():

    while True:

        UserInput = int(input("Enter 1 - to get weather info,\n 2 - to exit : "))

        if UserInput == 1:
            PresentInfo()

        elif UserInput == 2:
            break

        else:
            print("Invalid Input...Try Again")
            continue
    
if __name__=="__main__":
    main()            

        


