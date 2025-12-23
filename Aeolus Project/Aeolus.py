# CustomTkinter GUI (Graphical User Interface)
import customtkinter as ctk
from tkinter import messagebox

# Requests library (HTTP requests)
import requests

# .Env file loader (Hidden keys and variables)
import os 
from dotenv import load_dotenv
load_dotenv()

# Get current directory path
current_dir = os.path.dirname(os.path.abspath(__file__))

# WEATHER API SETUP
OpenWeatherKey = os.getenv("OpenWeatherKey")

DEFAULT_CITY = "Lisbon"

baseUrl = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": DEFAULT_CITY,
    "appid": OpenWeatherKey,    
    "units": "metric",
    "lang": "en"
}

def getWeatherDataByCity(city):
    params["q"] = city
    response = requests.get(baseUrl, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", "City not found or API error.")
        return None
    
def OrganizeWeatherData(data):
    if data:
        weather = {
            "city": data["name"],
            "temperature": round(data["main"]["temp"]),
            "description": data["weather"][0]["description"].title(),
            "temperatureMin": round(data["main"]["temp_min"]),
            "temperatureMax": round(data["main"]["temp_max"]),
            #Values for Boxes
            "realFeel": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "windSpeed": data["wind"]["speed"]


        }
        return weather
    return None

def getWeatherByCity(city):
    data = getWeatherDataByCity(city)
    weather = OrganizeWeatherData(data)
    return weather


# GUI SETUP
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AeolusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Config
        self.title("Aeolus - Weather App")
        self.geometry("400x600") #TODO: Adjust Size to correct fit the content
        self.resizable(False, False) #TODO: Make Responsive Design

        # The path to the icon inside that directory
        icon_path = os.path.join(current_dir, "Images", "AeolusLogo.ico")
        self.iconbitmap(default=icon_path)

        # FONTS
        self.font_temp = ("Arial", 70, "bold")
        self.font_city = ("Arial", 24)
        self.font_desc = ("Arial", 16)
        self.font_details = ("Arial", 14)

        # Inside the Window


if __name__ == "__main__":
    app = AeolusApp()
    app.mainloop()
