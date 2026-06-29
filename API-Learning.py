import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai
import csv
import GoogleCalendar
import json
from PIL import Image
import base64


load_dotenv()


API_KEY = os.getenv("API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
CALENDAR_KEY = os.getenv("CALENDAR_API_KEY")
POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT")
CF_API_KEY = os.getenv("CLOUDFLARE_API")
client = genai.Client(api_key = LLM_KEY)
userImageURL = "https://res.cloudinary.com/dytqwfesq/image/upload/v1782742488/PXL_20260629_140159088_bjfdzv.jpg"


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
    print(jsonOutput)
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


def showImageWithCloudflare(data):
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    prompt = "Replace the clothing of the person in the image with a cream linen shirt and grey shorts. Keep the exact same person, face, hairstyle, skin tone, body shape, pose and background. Only change the clothing to a cream linen shirt and grey shorts. Photorealistic photograph. Realistic face. Realistic human proportions. Do not change identity."
    userImage = getUserImage()
    print(type(userImage))
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/runwayml/stable-diffusion-v1-5-img2img"
    imageResponse = requests.post(
        url,
        headers={
            "Authorization":f"Bearer {CF_API_KEY}"
        },
        json={
            "prompt":prompt,
            "image_b64" : userImage,
        },
    )
    print(imageResponse.status_code)
    print(imageResponse.headers.get("content-type"))
    print(imageResponse.text[:500])
    with open("outfit.png", "wb") as f:
        f.write(imageResponse.content) #Gets the binary data

def showImageWithPollinations(data):
    files = [
        ("image", open("images/user.jpg", "rb")),
        ("image", open("images/black-sweater.jpg", "rb")),
    ] # Multipart-form data
    #mainTop = data["primary_outfit"]["top"]
    #mainBottoms = data["primary_outfit"]["bottom"]
    #prompt = f"Replace the clothing of the person in the image with a {mainTop} and {mainBottoms}. Keep the exact same person, face, hairstyle, skin tone, body shape, pose and background. Only change the clothing. Photorealistic photograph. Realistic face. Realistic human proportions. Do not change identity. Show the person's shoes and both feet."
    #userImage = getUserImage()
    testPrompt = "Replace the person's top with the sweatshirt shown in the reference image. Replace the bottoms with blue jeans"
    #print(type(userImage))
    postImage = requests.post( # Post used for editing image
        "https://gen.pollinations.ai/v1/images/edits",
        headers = {
            "Authorization" : f"Bearer {POLLINATIONS_KEY}"
        },
        data = {
            "prompt" : testPrompt,
            "model" : "nanobanana",
            "quality" : "high",
            #"image" : [userImageURL,"https://res.cloudinary.com/dytqwfesq/image/upload/v1782763960/PXL_20260629_200815120_em4hrt.jpg"],
        },
        files = files,
    )
    #Main image is as a b64 image or a URL
    print(postImage.status_code)
    print(postImage.text)
    response = postImage.json()
    b64Image = response["data"][0]["b64_json"] # Data is stored this way so am using dictionary manipluation to access it
    image = base64.b64decode(b64Image)
    with open("outfit.png", "wb") as f:
        f.write(image) #Gets the binary data
    
def getUserImage():
    with open("user.jpg", "rb") as f:
        base64Image = base64.b64encode(f.read()).decode("utf-8")
    return base64Image


response = requests.get("http://api.openweathermap.org/data/2.5/weather", params=parameters)
if response.status_code == 200:
    #print(response.content)
    jsonData = response.json() # Returns a dictionary so it can be queried using those
    temperature = jsonData["main"]["temp"]
    weather = jsonData["weather"][0]["description"]
    print(weather, temperature)
    userClothes = getClothes()
    try:
        #output = generateLLMResponse(weather, temperature, location, userClothes)
        #showImage({})
        showImageWithPollinations({})
        image = Image.open("outfit.png")
        image.show()
    except ServerError:
        print("The server is currently experiencing high demand, please try later")

    
    
else:
    print("Invalid city")


