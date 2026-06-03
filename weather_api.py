import requests
import sqlite3 as sq
import requests
import pandas as pd
import logging
import os
from datetime import datetime , timezone
from dotenv import load_dotenv


load_dotenv()

API_key = os.getenv("API_KEY")

direct_base_url = "http://api.openweathermap.org/geo/1.0/direct?"

coord_base_url = "https://api.openweathermap.org/data/2.5/weather?"


ENV = os.environ.get("ENV", "development").lower()

if ENV == "development":
    LOGLEVEL = logging.DEBUG
else:
    LOGLEVEL = logging.WARNING

logging.basicConfig(
    level=LOGLEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="weather_app.log",
    filemode="a"
)


def FindCoord(City_Name):
    try:
        Name_Based_url = f"{direct_base_url}q={City_Name}&limit=1&appid={API_key}"

        res = requests.get(Name_Based_url)
        res.raise_for_status()
        info = res.json()
        if res.status_code == 200:
            if not info :
                print("City not found")
                logging.warning(f"{City_Name} not found")
                return None

            coord = info[0]
            StateName = coord.get("state") or "Unknown"
            return [coord["lat"], coord["lon"]] , StateName
        

    except requests.exceptions.RequestException as e:
        print(f"Geo API Error : {e}")
        logging.error(f"Geo API Error: {res.text}")
        return None
    

def get_weather_info(coordinate):
    try:
        coord_url = f"{coord_base_url}lat={coordinate[0]}&lon={coordinate[1]}&appid={API_key}&units=metric"

        res = requests.get(coord_url , timeout=10)
        res.raise_for_status()

        return res.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Weather API Error : {e}")
        logging.error(f"Weather API Error: {e}")
        return None


def format_unix_time(unix_ts):
    return datetime.fromtimestamp(unix_ts, tz=timezone.utc).strftime("%H:%M:%S")


def WeatherAnalysis(city_name,weather_info,State_Name):
    return {
    "State":State_Name,
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
    "Sunrise": format_unix_time(weather_info["sys"]["sunrise"]),
    "Sunset": format_unix_time(weather_info["sys"]["sunset"])
    }


Db_Name = "Weather_Data.db"
Table_name = "weather"


def PresentInfo():
    City_Name = input("Enter the name of the city: ").strip()
    coordinates , StateName = FindCoord(City_Name)
    if not StateName:
        StateName = "Unknown"

    if coordinates == None:
        print("coordinate not found Enter Valid City Name.....exiting")
        return

    weather_info = get_weather_info(coordinates)

    data = pd.DataFrame([WeatherAnalysis(City_Name,weather_info,StateName)])
    data.insert(2,"Date",datetime.now().strftime("%Y-%m-%d"))

    SaveToDb(data)
    print(f"Saved to {Db_Name} in table '{Table_name}'")

    print(data.to_string())
    

def SaveToDb(df):
    try:
        conn = sq.connect(Db_Name)
        cur = conn.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        "State Name" TEXT NOT NULL,
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
        ("State Name","City Name", Date, Temp, Feels_Like, Pressure, Humidity, Description,
        Wind_Speed, Wind_Degree, Cloudiness, Visibility, Sunrise, Sunset)
        VALUES (? , ? , ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,(row["State"],row["City Name"], row["Date"], row["Temp"], row["Feels_Like"],
        row["Pressure"], row["Humidity"], row["Description"],
        row["Wind_Speed"], row["Wind_Deg"], row["Cloudiness"],
        row["Visibility"], row["Sunrise"], row["Sunset"]))

        conn.commit()
        
    except sq.Error as e:
        print(f"Database Error : {e}")
        logging.exception("Database error while saving weather data")
    
    finally:
        conn.close()


def ViewSaveData():

    try:
        conn = sq.connect(Db_Name)
        df = pd.read_sql_query("SELECT * FROM weather ORDER BY Date DESC", conn)
        print(df.to_string())

    except Exception as e:
        logging.exception(f"DataBase Error : {e}")
        print("Failed to Retrive.....\n")
    
    finally:
        conn.close()


def main():

    while True:
        try:
            UserInput = int(input
                ("1 - Get weather info\n"
                "2 - View saved data\n"
                "3 - to exit\n"
                "Enter Choice : ")
            )
        
        except ValueError:
            print("Invalid Input...Try Again")
            continue

        if UserInput == 1: PresentInfo()

        elif UserInput == 2: ViewSaveData()

        elif UserInput == 3: break

        else: print("Invalid Input...Try Again")

    
if __name__=="__main__":
    main()            

        


