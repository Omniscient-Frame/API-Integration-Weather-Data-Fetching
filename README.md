# Weather API Project

A beginner-friendly Python project that fetches real-time weather data using the OpenWeather API, stores results in a database, and helps you practice working with APIs, JSON, pandas, and SQLite.

## Overview

This project is a learning-based weather data fetcher built in Python.  
It takes city names from the user, gets their coordinates through OpenWeather geocoding, then fetches current weather data for those coordinates.

The project is designed to teach:
- How APIs work.
- How to use `requests` in Python.
- How to handle JSON responses.
- How to use pandas with API data.
- How to store data in SQLite.
- How to manage secrets with a `.env` file.

## Features

- Accepts one or more city names from the user.
- Fetches coordinates using OpenWeather geocoding API.
- Fetches current weather data using latitude and longitude.
- Extracts useful weather fields like temperature, humidity, and description.
- Stores weather data in a SQLite database.
- Can also export data to CSV during practice.
- Uses `.env` file to keep the API key private.

## Technologies Used

- Python
- Requests
- Pandas
- SQLite3
- python-dotenv
- OpenWeather API

## Project Flow

1. User enters a city name.
2. The program sends a request to the geocoding API.
3. The API returns latitude and longitude.
4. The program sends another request to the weather API.
5. The JSON response is converted into useful data.
6. The data is saved into a database.

## API Used

This project uses OpenWeather endpoints:

- Geocoding API: converts city names into coordinates.
- Current Weather API: returns live weather information for those coordinates.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Omniscient-Frame/API-Integration-Weather-Data-Fetching.git
```

### 2. Install dependencies

```bash
pip install requests pandas python-dotenv
```

### 3. Create a `.env` file

Create a file named `.env` in the project root:

```env
API_KEY=your_openweather_api_key_here
```

### 4. Add `.env` to `.gitignore`

```gitignore
.env
__pycache__/
*.db
```

### 5. Run the script

```bash
python weather_api.py
```

## Example Output

```text
Enter 1 - to get weather info,
 2 - to exit : 1
Enter the name of the city: agra
Saved to Weather_Data.db in table 'Weather'
  City Name        Date   Temp  Feels_Like  Pressure  Humidity       Description  Wind_Speed  Wind_Deg  Cloudiness  Visibility     Sunrise      Sunset
0      agra  2026-06-02  34.02       36.27      1002        43  scattered clouds        3.09       260          40        6000  1780358021  1780407507
```

## Database Storage

The project stores weather results in a SQLite database file.  
Each row represents one weather record for a city.

Example table fields:
- City Name
- Temperature
- Feels like
- Humidity
- Pressure
- Description
- Wind speed

## Learning Goals

This project was built to practice:
- making HTTP requests,
- reading API documentation,
- parsing JSON,
- using pandas DataFrames,
- saving structured data,
- and managing secrets safely.

## Future Improvements

Possible next steps:
- Add weather forecasts.
- Save multiple records over time.
- Build a GUI using Tkinter or Streamlit.
- Add charts for temperature history.
- Support more error handling and logging.

## Notes

- Make sure your API key is valid and active.
- Do not commit `.env` to GitHub.
- If the API returns an error, check the response status code and message.

## License

This project is for learning and practice.
