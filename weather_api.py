import sqlite3 as sq
import requests
import pandas as pd
import numpy as np
import csv 
import os
from dotenv import load_dotenv

np.random.seed(69)

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

conn =  sq.connect("Weather_Data.db")
cities = []

def WeatherAnalysis(city_name,weather_info):
    return {
    "City Name": city_name,
    "Temp": weather_info["main"]["temp"],
    "Feels Like": weather_info["main"]["feels_like"],
    "Pressure": weather_info["main"]["pressure"],
    "Humidity": weather_info["main"]["humidity"],
    "Description": weather_info["weather"][0]["description"],
    "Wind Speed": weather_info["wind"]["speed"],
    "Wind Deg": weather_info["wind"].get("deg"),
    "Cloudiness": weather_info["clouds"]["all"],
    "Visibility": weather_info["visibility"],
    "Sunrise": weather_info["sys"]["sunrise"],
    "Sunset": weather_info["sys"]["sunset"]
    }

def main():
    City_Name = input("Enter the name of the city: ").strip()
    coordinates = FindCoord(City_Name)

    if coordinates == None:
        print("coordinate not found...skipping")
        return

    weather_info = get_weather_info(coordinates)

    data = pd.DataFrame([WeatherAnalysis(City_Name,weather_info)])

    print(data.to_string())

if __name__=="__main__":
    main()
            
            
        
        


