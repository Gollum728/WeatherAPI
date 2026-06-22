import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai
import csv
import GoogleCalendar
import json
from PIL import Image


load_dotenv()


API_KEY = os.getenv("API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
CALENDAR_KEY = os.getenv("CALENDAR_API_KEY")
POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT")
CF_API_KEY = os.getenv("CLOUDFLARE_API")
client = genai.Client(api_key = LLM_KEY)


def generateLLMResponse(weather, temperature, location, clothes):
    jsonFormat = """Return your answer as valid JSON in the following format:
    {
  "primary_outfit": {
    "top": "",
    "bottom": "",
    "packedClothes" : [],
    "confidence": 0
  },
  "backup_outfit": {
    "top": "",
    "bottom": "",
    "packedClothes" : [],
    "confidence": 0
  }
}"""
    llmResponse = client.models.generate_content_stream(
        model = "gemini-3.5-flash",
        contents = f"I am currently in {location}. The weather is {weather} and it is {temperature} degrees celsius. Here is a list of the clothes that I own : {clothes}. Here are the events that I have today {GoogleCalendar.main()}. Based on this, give me 2 outfit recommendations using the clothes that I have - 1 outfit that would suit the weather conditions and the events I have today perfectly, and 1 backup option. If necessary, I can pack a bag with another set of clothes if an event I have requires a change of clothes, but don't include multiple outfit changes - I can only take 1 bag with 1 outfit inside! Give me a confidence score out of 10 for both of these options. Don't add extra details about the clothes, only use the details that are provided. Return your response in a JSON format like this: {jsonFormat}. Return only the JSON object. Don't include markdown or any explanations!"
    )

    output = ""
    for chunks in llmResponse:
        output += chunks.text
    jsonOutput = json.loads(output)
    return jsonOutput


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


def showImageWithGemini(data):
    mainTop = data["primary_outfit"]["top"]
    mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"Generate a picture of a person wearing {mainTop} and {mainBottoms}. "
    """
    if len(data["primary_outfit"]["packeClothes"]) > 0: # TO BE ADDED IN A SEPARATE FUNCTION!!
        prompt+=f"Generate a se"
    """
    imageResponse = client.models.generate_content(
        model = "gemini-2.5-flash-image-preview-image",
        contents= [prompt],
    )

    for part in imageResponse.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = part.as_image()
            image.save("generated_image.png")
    return image


def showImage(data):
    mainTop = data["primary_outfit"]["top"]
    mainBottoms = data["primary_outfit"]["bottom"]
    prompt = f"Generate a picture of a person wearing {mainTop} and {mainBottoms}. "
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/lykon/dreamshaper-8-lcm"
    imageResponse = requests.post(
        url,
        headers={
            "Authorization":f"Bearer {CF_API_KEY}"
        },
        json={
            "prompt":prompt
        },
    )
    print(imageResponse.status_code)
    print(imageResponse.headers.get("content-type"))
    print(imageResponse.text[:500])
    with open("outfit.png", "wb") as f:
        f.write(imageResponse.content) #Gets the binary data

    


response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
if response.status_code == 200:
    #print(response.content)
    jsonData = response.json() # Returns a dictionary so it can be queried using those
    temperature = jsonData["main"]["temp"]
    weather = jsonData["weather"][0]["description"]
    print(weather, temperature)
    userClothes = getClothes()
    try:
        output = generateLLMResponse(weather, temperature, location, userClothes)
        showImage(output)
        image = Image.open("outfit.png")
        image.show()
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


