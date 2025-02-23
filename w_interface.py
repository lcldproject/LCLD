from w_database import *
from w_weather import *

import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox 

class Interface:
    # Constructor
    def __init__(self, height, width):
        # Initialise database
        self.db = Database('weather.db')
        
        # Obtain combined list of cities in db and defaults
        default_cities = ["Zagreb",
                          "Varaždin",
                          "Koprivnica",
                          "New York",
                          "Los Angeles",
                          "London",
                          "Dublin",
                          "Kiev",
                          "Belgrade",
                          "Sarajevo"]
        db_cities = self.db.get_cities()
        
        #Remove duplicates
        self.cities = list(set(default_cities + db_cities))
        
        #Sort result
        self.cities.sort()
        
        # Create parent window
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.minsize(500,250)
        self.root.maxsize(500,250)
        
        # Create master frame
        self.iFMas = tk.Frame(self.root, bd = 8)
        self.iFMas.pack(fill = tk.BOTH, expand = True)
        
        # Add city widgets
        self.iCityLabel = tk.Label(self.iFMas, text = 'City : ', font=("Arial", 12), bd = 4)
        self.iCityLabel.grid(row = 0, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)
        self.combo_box = ttk.Combobox(self.iFMas, values = self.cities)
        self.combo_box.grid(row = 0, column = 1, columnspan = 2, sticky = tk.W+tk.E)
        
        # Set default value for combobox
        if(len(self.cities) > 0):
            self.combo_box.set(self.cities[0])
        
        # Bind event function to combobox
        self.combo_box.bind('<<ComboboxSelected>>', self.combo_box_input)
        self.combo_box.bind('<Return>', self.combo_box_input)
        
        # Add atmospheric widgets
        self.iHSky = tk.Label(self.iFMas, text = "Atmosphere", font=("Arial", 12), bd = 4)
        self.iHSky.grid(row = 1, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iDesc = tk.Label(self.iFMas, text = "", font=("Arial", 16), bd = 4)
        self.iDesc.grid(row = 2, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iIconImg = PhotoImage(file = "00d.png")
        self.iIcon = tk.Label(self.iFMas, image = self.iIconImg, bd = 4)
        self.iIcon.grid(row = 3, column = 0, sticky = tk.N+tk.S+tk.W+tk.E)
        
        # Add temperature widgets (The "Humidity" text here was switched with the "Temperature" one during the finishing edits, due to its placement on the widget)
        self.iHTmp = tk.Label(self.iFMas, text = "Humidity", font=("Arial", 12), bd = 4)
        self.iHTmp.grid(row = 1, column = 1, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iHumi = tk.Label(self.iFMas, text = "", font=("Arial", 16), bd = 4)
        self.iHumi.grid(row = 2, column = 1, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iTemp = tk.Label(self.iFMas, text = "", font=("Arial", 32), bd = 4)
        self.iTemp.grid(row = 3, column = 1, sticky = tk.N+tk.S+tk.W+tk.E)
        
        # Add wind widgets
        self.iHWnd = tk.Label(self.iFMas, text = "Wind", font=("Arial", 12), bd = 4)
        self.iHWnd.grid(row = 1, column = 2, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iWDir = tk.Label(self.iFMas, text = "", font=("Arial", 16), bd = 4)
        self.iWDir.grid(row = 2, column = 2, sticky = tk.N+tk.S+tk.W+tk.E)
        self.iWSpd = tk.Label(self.iFMas, text = "", font=("Arial", 32), bd = 4)
        self.iWSpd.grid(row = 3, column = 2, sticky = tk.N+tk.S+tk.W+tk.E)
        
        # Congfigure grid
        self.iFMas.columnconfigure(0, weight = 1)
        self.iFMas.columnconfigure(1, weight = 1)
        self.iFMas.columnconfigure(2, weight = 1)
        self.iFMas.rowconfigure(0, weight = 1)
        self.iFMas.rowconfigure(1, weight = 1)
        self.iFMas.rowconfigure(2, weight = 2)
        self.iFMas.rowconfigure(3, weight = 3)
        
        # Trigger initial search
        self.combo_box_input(None)
        
        #Test
        #testWeather = Weather.get_weather("Zagreb")
        #testWeather = Weather.get_weather("Wakanda")
        #self.update_weather(testWeather)
        
        # Launch interface
        self.root.mainloop()
        
    # Respond to user input in combo-box
    def combo_box_input(self, event):
        # Obtain new input
        newInput = self.combo_box.get()
        
        # Attempt to get new weather
        newWeather = Weather.get_weather(newInput)
        
        # Check valid weather object was found
        if isinstance(newWeather, Weather):
            # Valid weather object
            # Record change
            self.currentCity = newInput
            
            # Update db
            self.db.update_weather(newWeather)
            
            # Update cities
            if not (newInput in self.cities):
                # Add to cities
                self.cities.append(newInput)
                self.cities.sort()

                # Add to combobox
                self.combo_box.config(values = self.cities)
            
            # Update interface
            self.update_weather(newWeather)
        else:
            # Invalid weather object
            # Reset combo box
            self.combo_box.set(self.currentCity)
            
            # Inform user
            messagebox.showerror("City not found", "Sorry, we were not able to find " + newInput) 
        return
    
    #Update interface with new weather object
    def update_weather(self, weather):
        #Check weather exists
        if isinstance(weather, Weather):
            # Update widgets
            self.iDesc.config(text = weather.desc)
            self.iIconImg = PhotoImage(file = weather.path)
            self.iIcon.config(image = self.iIconImg)
            self.iHumi.config(text = str(weather.humi) + " %")
            self.iTemp.config(text = str(weather.temp) + " ºC")
            self.iWDir.config(text = weather.wDir)
            self.iWSpd.config(text = str(weather.wSpd) + " Km/h")
            return
        elif weather:
            # Blank widgets
            self.iDesc.config(text = "")
            self.iIconImg = PhotoImage(file = "00d.png")
            self.iIcon.config(image = self.iIconImg)
            self.iHumi.config(text = "")
            self.iTemp.config(text = "")
            self.iWDir.config(text = "")
            self.iWSpd.config(text = "")
            return
    
    #Properly exit app
    def quit(self):
        self.root.destroy()