# Operating System library
import os

# Requests library (HTTP requests)
import requests

# Logging library
import logging

# .Env file loader (Hidden keys and variables)
from dotenv import load_dotenv
load_dotenv()

# Setup logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AeolusService():
    def __init__(self):
        self.api_key = os.getenv("OpenWeatherKey")
        self.weather_url = "https://api.openweathermap.org/data/2.5"

        if not self.api_key:
            logging.error("OpenWeatherKey not found. Please check .env file.")

        self.session = requests.Session()
    
    def _get_request(self, endpoint, params):
        params['appid'] = self.api_key

        url = f"{self.weather_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status() 
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API Request failed: {e}")
            return None
    
    # Get Weather by City Name (default: London)
    def get_weather_by_city(self, city = "London"):
        params = {
            "q": city,
            "units": "metric",
            "lang": "en"
        }

        data = self._get_request("weather", params)

        if data:
            organized_data = self._organize_weather_data(data)
            return organized_data
        else:
            logging.error(f"No weather data found for city: {city}")
            return None
        

    # Organize Weather Data
    def _organize_weather_data(self, data):
        if not data:
            logging.error("No data to organize.")
            return None
        
        organized_data = {
            #Must have content:
            "statusCode": data.get("cod"),
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            # Main content:
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

        return organized_data

    #Get 4 day forecast by  City
    def get_4Day_forecast(self, city = "London"):
        params = {
            "q" : city,
            "units" : "metric",
            "lang" : "en",
            "cnt" : 4
        }

        data = self._get_request("forecast", params)
        if data:
            organized_forecast = self.organize_forecast_data(data)
            return organized_forecast
        else:
            logging.error(f"No forecast data found for city: {city}")
            return None
            

    def organize_forecast_data(self, data):
        if not data:
            logging.error("No forecast data to organize.")
            return None
        
        organized_forecast = []

        for entry in data["list"]:
            forecast_entry = {
                "dateTime": entry["dt_txt"],
                "temperature": round(entry["main"]["temp"]),
                "weatherIcon": entry["weather"][0]["icon"],
                "description": entry["weather"][0]["description"].title(),
                "temperatureMin": round(entry["main"]["temp_min"]),
                "temperatureMax": round(entry["main"]["temp_max"])
            }
            organized_forecast.append(forecast_entry)
        


    # Get weather icon image from OpenWeather
    def get_icon_image(self, icon_code):
        url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
        try:
            response = self.session.get(url, stream=True)
            if response.status_code == 200:
                return response.content 
        except requests.RequestException:
            return None