import os
import io
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from Logic import Aeolus_Service as weatherService
from datetime import datetime


# Get today's date in a readable format
month = datetime.now().strftime("%b")
day = datetime.now().strftime("%d").lstrip("0")
today_text = f"Today, {month} {day}"

# CustomTkinter Configuration
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class AeolusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ###################
        ## Window Config ##
        ###################
        self.title("Aeolus - Weather App")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.configure(bg="#FFFFFF")

        # Icon Setup
        currentDir = os.path.dirname(os.path.abspath(__file__))
        imageFolderPath = os.path.join(os.path.dirname(currentDir), "images")
        iconPath = os.path.join(currentDir, "..", "Images", "AeolusLogo.ico")
        try:
            self.iconbitmap(default=iconPath)
        except Exception:
            print("Warning: Icon file not found or could not be set.")
            pass

        # Fonts
        self.fontDate = ("Arial", 14)
        self.fontTemp = ("Arial", 70, "bold")
        self.fontCity = ("Arial", 20, "bold")
        self.fontCountry = ("Arial", 12)
        self.fontDesc = ("Arial", 16)
        self.fontStatsText = ("Arial", 16, "bold")
        self.fontStatsValue = ("Arial", 14)
        self.fontDetails = ("Arial", 14)


        # Get Images for Buttins
        nightDayImagePath = os.path.join(imageFolderPath, "night-day.png")
        searchImagePath = os.path.join(imageFolderPath, "search.png")

        # Load the Image using CTkImages
        nightDayIcon = ctk.CTkImage(light_image=Image.open(nightDayImagePath),
                                dark_image=Image.open(nightDayImagePath),
                                size=(24, 24))
        searchIcon = ctk.CTkImage(light_image=Image.open(searchImagePath),
                                dark_image=Image.open(searchImagePath),
                                size=(24, 24))
        
        WindIcon = ctk.CTkImage(light_image=Image.open(os.path.join(imageFolderPath, "wind.png")),
                                dark_image=Image.open(os.path.join(imageFolderPath, "wind.png")),
                                size=(15, 15))
        
        HumidityIcon = ctk.CTkImage(light_image=Image.open(os.path.join(imageFolderPath, "humi.png")),
                                dark_image=Image.open(os.path.join(imageFolderPath, "humi.png")),
                                size=(15, 15))
        
        RealFeelIcon = ctk.CTkImage(light_image=Image.open(os.path.join(imageFolderPath, "realfeel.png")),
                                dark_image=Image.open(os.path.join(imageFolderPath, "realfeel.png")),
                                size=(15, 15))
        
        
        
        ########################
        ## Inside window setup##
        ########################

        # Grid config
        # Columns
        self.grid_columnconfigure(0, weight=5) 
        self.grid_columnconfigure(1, weight=1)
        # Rows
        self.grid_rowconfigure(0, weight=500)

        # Top left grid
        frameLeft = ctk.CTkFrame(self, fg_color="#F0F0F0")
        frameLeft.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Header Section (Of the left frame)
        headerFrame = ctk.CTkFrame(master=frameLeft, fg_color="transparent")
        headerFrame.pack(fill="x", padx=20, pady=(10, 2))

        headerFrame.columnconfigure(0, weight=1) # Left spacer
        headerFrame.columnconfigure(1, weight=1) # Center spacer
        headerFrame.columnconfigure(2, weight=1) # Right spacer

        #TODO: Add functionality to the buttons
        # Search Button (Left)
        btnSearch = ctk.CTkButton(headerFrame, image=(searchIcon), text="", width=30, 
                                  fg_color="transparent", text_color="black", hover=False, hover_color="light grey")
        btnSearch.grid(row=0, column=0, sticky="w")

        # Location Text (Center)
        locationFrame = ctk.CTkFrame(headerFrame, fg_color="transparent")
        locationFrame.grid(row=0, column=1)

        self.locationLabel = ctk.CTkLabel(locationFrame, text="Loading...", font=self.fontCity, text_color="black")
        self.locationLabel.pack()
        self.locationCountry = ctk.CTkLabel(locationFrame, text="Loading...", font=self.fontCountry, text_color="gray")
        self.locationCountry.pack()

        # Settings Button (Right)
        btnColorType = ctk.CTkButton(headerFrame, image=(nightDayIcon), text= "", width=30, fg_color="transparent",
                                      text_color="black", hover=True, hover_color="light grey")
        btnColorType.grid(row=0, column=2, sticky="e")

        # MAIN WEATHER CARD
        weatherCard = ctk.CTkFrame(master=frameLeft, fg_color="#407BFF", corner_radius=30)
        weatherCard.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Content inside the weather card
        # Date
        ctk.CTkLabel(weatherCard, text=today_text, font=self.fontDate, text_color="white").pack(pady=(20, 5))

        # Icon of the weather
        self.weatherIconLabel = ctk.CTkLabel(weatherCard, text="", image=None)
        self.weatherIconLabel.pack(pady=(0, 0))

        # Temperature
        self.weatherTempLabel = ctk.CTkLabel(weatherCard, text="Loading...", font=self.fontTemp, text_color="white")
        self.weatherTempLabel.pack(pady=(0, 0))
        self.weatherDescriptionLabel = ctk.CTkLabel(weatherCard, text="Loading...", font=self.fontDesc, text_color="white")
        self.weatherDescriptionLabel.pack(pady=(0, 10))

        #Minimum and Maximum Temperature
        tempMinMaxFrame = ctk.CTkFrame(master=weatherCard, fg_color="#6B99FF",corner_radius=20)
        tempMinMaxFrame.pack(pady=(10, 10), padx=20)

        self.tempMinLabel = ctk.CTkLabel(tempMinMaxFrame, text="↑ --°", font=self.fontDetails, text_color="white")
        self.tempMinLabel.pack(side="left", padx=(20, 20), pady=10)
        separator = ctk.CTkLabel(tempMinMaxFrame, text="|", font=self.fontDetails, text_color="white")
        separator.pack(side="left", pady=10)
        self.tempMaxLabel = ctk.CTkLabel(tempMinMaxFrame, text="↓ --°", font=self.fontDetails, text_color="white")
        self.tempMaxLabel.pack(side="left", padx=(20, 20), pady=10)

        # STATS of Today ROW
        stats_container = ctk.CTkFrame(master=frameLeft, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 20))

        # Configure grid for the 3 cards to space them evenly
        stats_container.columnconfigure((0, 1, 2), weight=1)

        # Helper function to create the small cards to avoid repeating code
        def create_stat_card(parent, icon, value_text, label_text):
            card = ctk.CTkFrame(master=parent, fg_color="#FFFFFF", corner_radius=15)
            card.grid_columnconfigure(0, weight=1)
            card.grid(row=0, column=len(parent.grid_slaves()), padx=5, pady=5, sticky="nsew")
            
            icon_label = ctk.CTkLabel(card, image=icon, text="", fg_color="#E4F2FD", corner_radius=50)
            icon_label.pack(pady=(10, 0))

            value_label = ctk.CTkLabel(card, text=value_text, font=self.fontStatsValue, text_color="grey")
            value_label.pack(pady=(5, 0))
            
            text_label = ctk.CTkLabel(card, text=label_text, font=self.fontStatsText, text_color="black")
            text_label.pack(pady=(5, 10))
            
            return text_label
        
        self.humidityLabel = create_stat_card(stats_container, HumidityIcon, "Humidity", "--%")
        self.windSpeedLabel = create_stat_card(stats_container, WindIcon, "Wind Speed", "-- m/s")
        self.realFeelLabel = create_stat_card(stats_container, RealFeelIcon, "Real Feel", "--°C")

        # TODO: Start the right side frame content
        # Right side
        frameRight = ctk.CTkFrame(self, fg_color="white")
        frameRight.grid(row=0, column=1, rowspan=1, sticky="nsew", padx=5, pady=5)
    
        self.LoadDefaultWeather()

    ##################
    # Helper Methods #
    ##################
    def LoadDefaultWeather(self):
        data = weatherService.GetDefaultCityWeather()
        if data:
            self.UpdateWeatherUI(data)
        else:
            messagebox.showerror("Weather Error", "Unable to load default weather data.")
    

    # TODO: Add error handling for missing data and Add whats missing
    def UpdateWeatherUI(self, weatherData):
        # Update location labels in header
        self.locationLabel.configure(text=weatherData["city"])
        self.locationCountry.configure(text=weatherData["country"])
        
        #Main Card Updates
        # Get and set weather icon in main card
        iconCode = weatherData["weatherIcon"]
        iconImageData = weatherService.GetIconImage(iconCode)

        if iconImageData:
           
            imageData = io.BytesIO(iconImageData)
            finalizedImage = Image.open(imageData)
            
            weatherIcon = ctk.CTkImage(light_image=finalizedImage, 
                                      dark_image=finalizedImage, 
                                      size=(100, 100))
            
            self.weatherIconLabel.configure(image=weatherIcon, text="")
            self.weatherIconLabel.image = weatherIcon

        self.weatherTempLabel.configure(text=f"{weatherData['temperature']}°C")
        self.weatherDescriptionLabel.configure(text=weatherData["description"])
        self.tempMinLabel.configure(text=f"↓ {weatherData['temperatureMin']}°C")
        self.tempMaxLabel.configure(text=f"↑ {weatherData['temperatureMax']}°C")
        # Stats Updates
        self.humidityLabel.configure(text=f"{weatherData['humidity']}%")
        self.windSpeedLabel.configure(text=f"{weatherData['windSpeed']} m/s")
        self.realFeelLabel.configure(text=f"{weatherData['realFeel']}°C")