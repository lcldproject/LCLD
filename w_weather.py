import requests

class Weather:
    # Constructor
    def __init__(self, city, desc, path, humi, temp, wDir, wSpd):
        self.city = city
        self.desc = desc
        self.path = path
        self.humi = humi
        self.temp = self.format_temp(temp)
        self.wDir = self.format_w_dir(wDir)
        self.wSpd = self.format_w_spd(wSpd)
    
    # Convert from kelvin to celcius
    @staticmethod
    def format_temp(tempK):
        tempC = int(round(tempK - 273.15, 0))
        return tempC
    
    # Convert from degrees to compass
    @staticmethod
    def format_w_dir(dirDeg):
        dirRed=int((dirDeg/22.5)+.5) #Converts 0-359 -> 0-15 to access 0-15 in the array (For pairing with the directions)
        dirArr =["N","NNE","NE","ENE","E","ESE", "SE", "SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"]
        dirMag = dirArr[(dirRed % 16)]
        return dirMag
    
    # Convert from m/s to km/h
    @staticmethod
    def format_w_spd(spdMs):
        spdKmh = int(round(spdMs * 3.6, 0))
        return spdKmh
    
    # Get weather object from API
    @staticmethod
    def get_weather(city):
        # Create request URL
        reqStart = "https://api.openweathermap.org/data/2.5/weather?q="
        reqEnd = "&APPID="
        reqKey = "38ecec3cac02a05c7c1fa958d09743cc"
        reqURL = reqStart + city + reqEnd + reqKey
        
        # Attempt to retrieve data
        try:
            # Make a GET request
            res = requests.get(reqURL)

            # Check if the request was successful
            if res.status_code == 200:
                # Record data
                resData = res.json()
            else:
                # Record failure
                print('Error:', res.status_code)
                print(city + " doesn't seem to exist")
                return None
        except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            print('Error:', e)
            return None
        
        # Construct weather object
        resWeather = Weather(city,
                             resData['weather'][0]['description'],
                             str(resData['weather'][0]['icon']) + ".png",
                             resData['main']['humidity'],
                             resData['main']['temp'],
                             resData['wind']['deg'],
                             resData['wind']['speed'])
        
        # Return weather object
        return resWeather