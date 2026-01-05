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

class AeolusService:
    def __init__(self):
        self.api_key = os.getenv("OpenWeatherKey")
        self.weather_url = "https://api.openweathermap.org/data/2.5"
        self.geo_url = "https://api.openweathermap.org/geo/1.0/"
        
        if not self.api_key:
            logging.error("OpenWeatherKey not found. Please check .env file.")
        
        self.session = requests.Session()

    # Get Request to OpenWeather API
    def _get_request(self, base_url, endpoint, params):
        params['appid'] = self.api_key

        url = f"{base_url}/{endpoint}"

        try:
            response = self.session.get(url, params=params)
            response.raise_for_status() 
            return response.json()
        except requests.RequestException as e:
            logging.error(f"API Request failed: {e}")
            return None
    
    # Get coordinates for a city using Geocoding API
    def _get_coordinates(self, city):
            params = {
                "q": city,
                "limit": 1
            }
            
            data = self._get_request(self.geo_url, "direct", params)
            
            if data and len(data) > 0:
                return data[0]['lat'], data[0]['lon'], data[0]['name']
                
            logging.warning(f"No coordinates found for city: {city}")
            return None, None, None
        

    #TODO: Get Weather by Coords isn't as precise as by City, need to Implement both
    # keep the most precise as default and by coords as backup (Since by city was deprecated by OpenWeather and may stop working anytime, even if its more precise now)

    # Get weather by city name (Using Geocoding because of by city was deprecated by OpenWeather)
    def get_weather_data(self, city = "Porto,PT"):

        lat, lon, city_name = self._get_coordinates(city) # CityName is saved because the coords city name may differ from the input city name when fetching weather.

        if lat is None or lon is None:
            logging.error(f"Could not retrieve coordinates for city: {city}")
            return None
        
        params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "lang": "en"
        }

        data = self._get_request(self.weather_url, "weather", params)

        if data:
            return self._organize_weather_data(data, city_name)
        else:
            logging.error(f"Could not retrieve weather data for city: {city}")
            return None


    
    # Organize weather data
    def _organize_weather_data(self, data, city_name):
        if not data:
            logging.error("No data to organize.")
            return None
        
        return{
            #Must have content:
            "statusCode": data.get("cod"),
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            # Main content:
            "city": city_name,
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
    
    # Get weather icon image from OpenWeather
    def get_icon_image(self, icon_code):
        url = f"https://openweathermap.org/img/wn/{icon_code}@4x.png"
        try:
            response = self.session.get(url, stream=True)
            if response.status_code == 200:
                return response.content 
        except requests.RequestException:
            return None