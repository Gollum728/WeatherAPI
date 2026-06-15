import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai
import csv
load_dotenv()


API_KEY = os.getenv("API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
client = genai.Client(api_key = LLM_KEY)


def generateLLMResponse(weather, temperature, location, clothes):

    llmResponse = client.models.generate_content_stream(
        model = "gemini-3.5-flash",
        contents = f"I am currently in {location}. The weather is {weather} and it is {temperature} degrees celsius. Here is a list of my clothes that I currently have: {clothes}. Based on this, give me 2 outfit recommendations using the clothes I have - 1 outfit that would suit the weather conditions perfectly and 1 backup option for me to choose from. Take the colour of the outfit into consideration as well"
    )

    output = ""
    for chunks in llmResponse:
        output += chunks.text
    return output


def getClothes():
    clothesString = ""
    with open("clothes.csv", "r") as f:
        data = csv.reader(f)
        for row in data:
            newRow = ",".join(row)
            clothesString = clothesString + newRow + "\n"
    return clothesString
location = input("Enter a city : ")

parameters = {"q": location, "units":"metric", "appid":API_KEY} # Parameters that are declared to get specific data from the API


#PREVIOUS CHALLENGE
"""
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
"""



response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
if response.status_code == 200:
    #print(response.content)
    jsonData = response.json() # Returns a dictionary so it can be queried using those
    temperature = jsonData["main"]["temp"]
    weather = jsonData["weather"][0]["description"]
    print(weather, temperature)
    userClothes = getClothes()
    try:
        print(generateLLMResponse(weather, temperature, location, userClothes))
    except ServerError:
        print("The server is currently experiencing high demand, please try later")

    """
    accessories = determineAccessories(weather)
    attire = determineClothes(temperature)
    message = f"It is {temperature} degrees celsius and {weather}. Wear a {attire}"
    if accessories is not None:
        message += f" and bring {accessories}"
    print(message)
    """
    
    
else:
    print("Invalid city")


