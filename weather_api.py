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


def FindCoord(Name_Based_url):
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
    

def weather_analysis(coordinate):
    coord_url = f"{coord_base_url}lat={coordinate[0]}&lon={coordinate[1]}&appid={API_key}&units=metric"
    res = requests.get(coord_url)
    info = res.json()
    print("the response is : ",res.status_code)
    return info

conn =  sq.connect("Weather_Data.db")
cities = []

while True:
    print("write exit to quit")
    City_Name = input("Enter the name of the city: ").lower().strip()
    if(City_Name == "exit"):
        break
    cities.append(City_Name)
    
for city in cities:
    Name_Based_url = f"{direct_base_url}q={city}&limit=1&appid={API_key}"

    print("the url is : ",Name_Based_url)
    coordinates = FindCoord(Name_Based_url)

    if coordinates == None:
        print("coordinate not found...skipping")
        continue
        

    else:
        weather_info = weather_analysis(coordinates)
        df = pd.json_normalize(weather_info["main"])
        df["City Name"] = city
        
    if __name__ == "__main__":
            to_drop = ["temp_min","temp_max","sea_level","grnd_level"]
            df.drop(to_drop,axis=1,inplace=True,errors="ignore")

            #city name in 1st column 
            check_col = ["City Name"] + [c for c in df.columns if c != "City Name"]
            df = df[check_col]      

            if os.path.isfile("weather_data.csv"):
                
                existing_df = pd.read_csv("weather_data.csv")
                

                missing_cols = [c for c in df.columns if c not in existing_df.columns]
                print(missing_cols)

                existing_df = existing_df[df.columns]
                print(existing_df)

                combined_df = pd.concat([existing_df, df], ignore_index=True)
                
                combined_df.drop_duplicates(subset=["City Name"], keep="last", inplace=True)

                combined_df.to_csv("weather_data.csv", mode="a", header=True, index=False)

                print(combined_df)

            else:
                df.to_csv("weather_data.csv", mode="w", header=True, index=False)

            
            
        
        


