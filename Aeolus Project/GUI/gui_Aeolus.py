import os
import io
import json
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from Logic import Aeolus_Service as weatherservice
from datetime import datetime


# Get today's date in a readable format
month = datetime.now().strftime("%b")
day = datetime.now().strftime("%d").lstrip("0")
today_text = f"Today, {month} {day}"

# CustomTkinter Configuration
ctk.set_default_color_theme("blue")

class AeolusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        start_mode = self.load_state_mode()
        ctk.set_appearance_mode(start_mode)

        self.weather_service = weatherservice.AeolusService()

        ###################
        ## Window Config ##
        ###################
        self.title("Aeolus - Weather App")
        self.geometry("1200x600")
        self.resizable(False, False)
        self.configure(fg_color=("#FFFFFF", "#121212"))

        # Icon Setup
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_folder_path = os.path.join(os.path.dirname(current_dir), "images")
        icon_path = os.path.join(current_dir, "..", "Images", "AeolusLogo.ico")
        try:
            self.iconbitmap(default=icon_path)
        except Exception:
            print("Warning: Icon file not found or could not be set.")
            pass

        # Fonts
        self.font_date = ("Arial", 14)
        self.font_temp = ("Arial", 70, "bold")
        self.font_city = ("Arial", 20, "bold")
        self.font_country = ("Arial", 12)
        self.font_desc = ("Arial", 16)
        self.font_stats_text = ("Arial", 16, "bold")
        self.font_stats_value = ("Arial", 14)
        self.font_details = ("Arial", 14)


        # Get images for buttons
        night_day_image_path = os.path.join(image_folder_path, "night-day.png")
        search_image_path = os.path.join(image_folder_path, "search.png")

        # Load the image using CTkImages
        night_day_icon = ctk.CTkImage(light_image=Image.open(night_day_image_path),
                                dark_image=Image.open(night_day_image_path),
                                size=(24, 24))
        search_icon = ctk.CTkImage(light_image=Image.open(search_image_path),
                                dark_image=Image.open(search_image_path),
                                size=(24, 24))
        
        wind_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_folder_path, "wind.png")),
                                dark_image=Image.open(os.path.join(image_folder_path, "wind.png")),
                                size=(15, 15))
        
        humidity_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_folder_path, "humi.png")),
                                dark_image=Image.open(os.path.join(image_folder_path, "humi.png")),
                                size=(15, 15))
        
        real_feel_icon = ctk.CTkImage(light_image=Image.open(os.path.join(image_folder_path, "realfeel.png")),
                                dark_image=Image.open(os.path.join(image_folder_path, "realfeel.png")),
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
        frame_left = ctk.CTkFrame(self, fg_color=("#F0F0F0", "#1E1E1E"))
        frame_left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Header Section (Of the left frame)
        header_frame = ctk.CTkFrame(master=frame_left, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 2))

        header_frame.columnconfigure(0, weight=1) # Left spacer
        header_frame.columnconfigure(1, weight=1) # Center spacer
        header_frame.columnconfigure(2, weight=1) # Right spacer

        # Search Contents (Left)
        # Search Entry (Hidden by default)
        self.search_entry = ctk.CTkEntry(header_frame, width=150, placeholder_text="Enter city name...")
        self.search_entry.bind("<Return>", self.perform_search)  # Search on Enter
        self.search_entry.bind("<FocusOut>", self.close_search_bar) # Close if focus is lost

        # Search Button
        self.btn_search = ctk.CTkButton(header_frame, image=(search_icon), text="", width=30, 
                                  fg_color="transparent", text_color=("black", "white"), hover=False, hover_color="light grey",
                                  command=self.open_search_bar)
        
        # Grid the button by default
        self.btn_search.grid(row=0, column=0, sticky="w")

        # Location Text (Center)
        location_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        location_frame.grid(row=0, column=1)

        self.location_label = ctk.CTkLabel(location_frame, text="Loading...", font=self.font_city, text_color=("black", "white"))
        self.location_label.pack()
        self.location_country = ctk.CTkLabel(location_frame, text="Loading...", font=self.font_country, text_color=("gray", "lightgray"))
        self.location_country.pack()

        # Color Scheme Button (Right)
        btn_color_type = ctk.CTkButton(header_frame, image=(night_day_icon), text= "", width=30, fg_color="transparent",
                                      text_color=("black", "white"), hover=True, hover_color="light grey", command=self.toggle_night_day_mode)
        btn_color_type.grid(row=0, column=2, sticky="e")

        # Main Weather Card
        weather_card = ctk.CTkFrame(master=frame_left, fg_color=("#407BFF", "#821FBB"), corner_radius=30)
        weather_card.pack(fill="both", expand=True, padx=20, pady=(20, 10))

        # Content inside the weather card
        # Date
        ctk.CTkLabel(weather_card, text=today_text, font=self.font_date, text_color="white").pack(pady=(20, 5))

        # Icon of the weather
        self.weather_icon_label = ctk.CTkLabel(weather_card, text="", image=None)
        self.weather_icon_label.pack(pady=(0, 0))

        # Temperature
        self.weather_temp_label = ctk.CTkLabel(weather_card, text="Loading...", font=self.font_temp, text_color="white")
        self.weather_temp_label.pack(pady=(0, 0))
        self.weather_description_label = ctk.CTkLabel(weather_card, text="Loading...", font=self.font_desc, text_color="white")
        self.weather_description_label.pack(pady=(0, 10))

        # Minimum and Maximum Temperature
        temp_min_max_frame = ctk.CTkFrame(master=weather_card, fg_color=("#6B99FF", "#D386FF"),corner_radius=20)
        temp_min_max_frame.pack(pady=(10, 10), padx=20)

        self.temp_min_label = ctk.CTkLabel(temp_min_max_frame, text="↑ --°", font=self.font_details, text_color="white")
        self.temp_min_label.pack(side="left", padx=(20, 20), pady=10)
        separator = ctk.CTkLabel(temp_min_max_frame, text="|", font=self.font_details, text_color="white")
        separator.pack(side="left", pady=10)
        self.temp_max_label = ctk.CTkLabel(temp_min_max_frame, text="↓ --°", font=self.font_details, text_color="white")
        self.temp_max_label.pack(side="left", padx=(20, 20), pady=10)

        # STATS of Today ROW
        stats_container = ctk.CTkFrame(master=frame_left, fg_color="transparent")
        stats_container.pack(fill="x", padx=20, pady=(0, 20))

        # Configure grid for the 3 cards to space them evenly
        stats_container.columnconfigure((0, 1, 2), weight=1)

        # Helper function to create the small cards
        def create_stat_card(parent, icon, value_text, label_text):
            card = ctk.CTkFrame(master=parent, fg_color=("#FFFFFF", "#2B2B2B"), corner_radius=15)
            card.grid_columnconfigure(0, weight=1)
            card.grid(row=0, column=len(parent.grid_slaves()), padx=5, pady=5, sticky="nsew")
            
            icon_label = ctk.CTkLabel(card, image=icon, text="", fg_color=("#E4F2FD", "#4B4B4B"), corner_radius=50)
            icon_label.pack(pady=(10, 0))

            value_label = ctk.CTkLabel(card, text=value_text, font=self.font_stats_value, text_color=("black", "white"))
            value_label.pack(pady=(5, 0))
            
            text_label = ctk.CTkLabel(card, text=label_text, font=self.font_stats_text, text_color=("black", "white"))
            text_label.pack(pady=(5, 10))
            
            return text_label
        
        self.humidity_label = create_stat_card(stats_container, humidity_icon, "Humidity", "--%")
        self.wind_speed_label = create_stat_card(stats_container, wind_icon, "Wind Speed", "-- m/s")
        self.real_feel_label = create_stat_card(stats_container, real_feel_icon, "Real Feel", "--°C")

        # Right side
        frame_right = ctk.CTkFrame(self, fg_color=("white", "#1E1E1E"))
        frame_right.grid(row=0, column=1, rowspan=1, sticky="nsew", padx=5, pady=5)
    
        self.load_default_weather()

    ##################
    # Helper Methods #
    ##################
    def load_default_weather(self):
        try:
            last_location = self.load_last_location_weather()
        except Exception as e:
            print(f"Error loading last location weather: {e}")
            last_location = "London"

        if last_location is None:
            last_location = "London"

        data = self.weather_service.get_weather_by_city(last_location)

        if data:
            self.update_weather_ui(data)
        else:
            messagebox.showerror("Weather Error", "Unable to load default weather data.")

    def load_last_location_weather(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "json", "app_state.json")
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                last_location = data.get("last_location", "London")
                return last_location
        except FileNotFoundError:
            return "London"
    
    def load_user_weather(self, city):
        data = self.weather_service.get_weather_by_city(city)

        if data:
            self.update_weather_ui(data)
        else:
            messagebox.showerror("Weather Error", f"Unable to load weather data for {city}.")

    def update_weather_ui(self, weather_data):
        try:
            # Update location labels in header
            self.location_label.configure(text=weather_data["city"])
            self.location_country.configure(text=weather_data["country"])
            
            #Main Card Updates
            # Get and set weather icon in main card
            icon_code = weather_data["weatherIcon"]
            icon_image_data = self.weather_service.get_icon_image(icon_code)

            if icon_image_data:
            
                image_data = io.BytesIO(icon_image_data)
                finalized_image = Image.open(image_data)
                
                weather_icon = ctk.CTkImage(light_image=finalized_image, 
                                        dark_image=finalized_image, 
                                        size=(100, 100))
                
                self.weather_icon_label.configure(image=weather_icon, text="")
                self.weather_icon_label.image = weather_icon

            self.weather_temp_label.configure(text=f"{weather_data['temperature']}°C")
            self.weather_description_label.configure(text=weather_data["description"])
            self.temp_min_label.configure(text=f"↓ {weather_data['temperatureMin']}°C")
            self.temp_max_label.configure(text=f"↑ {weather_data['temperatureMax']}°C")
            # Stats Updates
            self.humidity_label.configure(text=f"{weather_data['humidity']}%")
            self.wind_speed_label.configure(text=f"{weather_data['windSpeed']} m/s")
            self.real_feel_label.configure(text=f"{weather_data['realFeel']}°C")
        except KeyError as e:
            messagebox.showerror("Data Error", f"Missing data in weather response: {e}")


    ######################
    #   Buttons Methods  #
    ######################

    # Search methods
    def open_search_bar(self):
        self.btn_search.grid_remove()
        self.search_entry.grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.search_entry.focus_set() 

    def close_search_bar(self, event=None):
        self.search_entry.grid_remove()
        self.search_entry.delete(0, "end") # Deleted to clear previous text
        self.btn_search.grid(row=0, column=0, sticky="w")

    def perform_search(self, event=None):
        city = self.search_entry.get()
        
        if city:
            # Load weather for inserted city
            self.load_user_weather(city)
            # Save the last location
            self.save_state(ctk.get_appearance_mode(), self.location_label.cget("text"))
        
        # Closes the bar and shows the button
        self.location_label.focus_set()
        self.close_search_bar()

    # Night and Day mode toggle method
    def toggle_night_day_mode(self):
        current_mode = ctk.get_appearance_mode()
        
        if current_mode == "Light":
            ctk.set_appearance_mode("Dark")
        else:
            ctk.set_appearance_mode("Light")
        
        # Save the current mode
        self.save_state(ctk.get_appearance_mode())
    
    # Load the last saved mode from JSON file
    def load_state_mode(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "json", "app_state.json")
        
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                return data.get("mode", "Light")
        except FileNotFoundError:
            return "Light"

    # Save the current mode and last location inside a JSON file
    def save_state(self, mode, last_location="London"):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_dir = os.path.join(current_dir, "json")
        file_path = os.path.join(json_dir, "app_state.json")

        try:
            # Create the directory if it doesn't exist
            if not os.path.exists(json_dir):
                os.makedirs(json_dir)

            with open(file_path, "w") as f:
                json.dump({"mode": mode, "last_location": last_location}, f)
        except Exception as e:
            print(f"Error saving state: {e}")