# Operating System library
import os

# Requests library (HTTP requests)
import requests

# .Env file loader (Hidden keys and variables)
from dotenv import load_dotenv
load_dotenv()

OpenWeatherKey = os.getenv("OpenWeatherKey")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# Functions related to weather data retrieval and organization
def GetWeatherData(city):
    params = {
        "q": city,
        "appid": OpenWeatherKey,    
        "units": "metric",
        "lang": "en"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException:
        "Error: Unable to connect to the weather service."

def OrganizeWeatherData(data):
    if not data:
        return None
        
    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature": round(data["main"]["temp"]),
        "weatherIcon": data["weather"][0]["icon"],
        "description": data["weather"][0]["description"].title(),
        "temperatureMin": round(data["main"]["temp_min"]),
        "temperatureMax": round(data["main"]["temp_max"]),
        # Containers content:
        "realFeel": round(data["main"]["feels_like"]),
        "humidity": data["main"]["humidity"],
        "windSpeed": data["wind"]["speed"]
    }

# Get weather for default city (Which is Lisbon), if you are wondering why, its because i want to
def GetDefaultCityWeather():
    data = GetWeatherData("Lisbon")
    return OrganizeWeatherData(data)

# Get weather by city name
def GetWeatherByCity(city):
    data = GetWeatherData(city)
    return OrganizeWeatherData(data)

# Get weather icon image from OpenWeather
def GetIconImage(icon_code):
    url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            return response.content 
    except requests.RequestException:
        return None