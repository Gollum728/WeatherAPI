import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file
from datetime import datetime
from datetime import timedelta


load_dotenv()
API_KEY = os.getenv("API_KEY")


def getCurrentWeather(location):
    weatherData = {}
    parameters = {"q": location, "units":"metric", "appid":API_KEY} # Parameters that are declared to get specific data from the API
    response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
    if response.status_code == 200:
        #print(response.content)
        jsonData = response.json() # Returns a dictionary so it can be queried using those
        temperature = jsonData["main"]["temp"]
        weather = jsonData["weather"][0]["description"]
        weatherData["Temperature"] = temperature
        weatherData["Weather"] = weather
        return weatherData
    else:
        print("Invalid city")

def getWeatherForDay(location):
    forecastString = ""
    parameters = {"q": location, "units":"metric", "appid":API_KEY, "cnt" : 40} # Parameters that are declared to get specific data from the API
    response = requests.get("http://api.openweathermap.org/data/2.5/forecast", params=parameters)
    nextDatetime = str(datetime.now() + timedelta(days=1))
    nextDay = nextDatetime.split()[0]
    if response.status_code == 200:
        jsonData = response.json()
        print(jsonData["city"]["name"])
        forecastData = jsonData["list"]
        for time in forecastData:
            dateTime = time["dt_txt"]
            date = dateTime.split()[0]
            if date == nextDay:
                temperature = time["main"]["temp"]
                weather = time["weather"][0]["description"]
                forecastTime = dateTime.split()[1][:5]  # e.g. "12:00"

                forecastString += (
                    f"{forecastTime}: {weather}, {temperature}°C\n"
                )
        
        print(forecastString)
        return forecastString



getWeatherForDay("Tenerife")