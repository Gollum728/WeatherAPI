import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai

from PIL import Image

import wardrobe
import weather
import clothing_recommendation as c_r
import image_generation as i_g


load_dotenv()


API_KEY = os.getenv("API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
CALENDAR_KEY = os.getenv("CALENDAR_API_KEY")
POLLINATIONS_KEY = os.getenv("POLLINATIONS_API_KEY")
CF_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT")
CF_API_KEY = os.getenv("CLOUDFLARE_API")
client = genai.Client(api_key = LLM_KEY)
userImageURL = "https://res.cloudinary.com/dytqwfesq/image/upload/v1782742488/PXL_20260629_140159088_bjfdzv.jpg"







def main():
    city = input("Enter a city : ")
    weatherData = weather.getWeather(city)
    clothes = wardrobe.getClothes()

    recommendation = c_r.generateLLMResponse(weatherData["weather"], weatherData["temperature"], city, clothes)
    
    userWardrobe = wardrobe.loadWardrobe()

    images = wardrobe.getClothingImages(userWardrobe, recommendation)
    
    i_g.showImageWithPollinations(images, recommendation)
    image = Image.open("outfit.png")
    image.show()

    

    
    

main()

