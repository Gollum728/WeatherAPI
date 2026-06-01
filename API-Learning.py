import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file

load_dotenv()
API_KEY = os.getenv("API_KEY")

location = input("Enter a city : ")

parameters = {"q": location, "units":"metric", "appid":API_KEY} # Parameters that are declared to get specific data from the API

def determineClothes(temperature):
    if temperature < 12:
        clothes = "jacket"
    elif temperature >= 12 and temperature < 17:
        clothes = "jumper"
    else:
        clothes = "t-shirt"
    return clothes

def determineAccessories(weather):
    if "rain" in weather or "clouds" in weather:
        accessories = "umbrella"
    elif "sun" in weather:
        accessories = "sunglasses"
    return accessories



response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
if response.status_code == 200:
    #print(response.content)
    jsonData = response.json() # Returns a dictionary so it can be queried using those
    temperature = jsonData["main"]["temp"]
    weather = jsonData["weather"][0]["description"]
    accessories = determineAccessories(weather)
    attire = determineClothes(temperature)
    message = f"It is {temperature} degrees celsius and {weather}. Wear a {attire}"
    if accessories is not None:
        message += f" and bring {accessories}"
    print(message)
    
    
else:
    response = "Invalid city"




print(response)


