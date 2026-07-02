import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file


load_dotenv()
API_KEY = os.getenv("API_KEY")


def getWeather(location):
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