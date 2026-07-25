import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai

from PIL import Image

import wardrobe
import weather
import clothing_recommendation as c_r
import image_generation as i_g
import GoogleCalendar
import send_email
import location


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
    userLocation = location.getLocation()
    attachmentImages = []
    #city = input("Enter a city : ")
    #weatherData = weather.getCurrentWeather(city)
    weatherData = weather.getWeatherForDay(userLocation)
    clothes = wardrobe.getClothes()

    calendarInfo = GoogleCalendar.main()
    events = calendarInfo["Events"]
    userEmail = calendarInfo["Email"]

    
    recommendation = c_r.generateLLMResponse(weatherData, userLocation, clothes, events)
    #print(recommendation)
    
    userWardrobe = wardrobe.loadWardrobe()


    
    i_g.generateBaseOutfit(userWardrobe, recommendation["primary_outfit"], "primary_outfit.png")
    primary_outerwear = recommendation["primary_outfit"]["outerwear"]
    if primary_outerwear is not None:
        i_g.generateOuterwear(userWardrobe, recommendation["primary_outfit"], "primary_outfit.png")
    attachmentImages.append("primary_outfit.png")

    if recommendation["primary_outfit"]["packed_outfit"] is not None:
        i_g.generateBaseOutfit(userWardrobe, recommendation["primary_outfit"]["packed_outfit"], "packed_outfit.png")
        packed_outerwear = recommendation["primary_outfit"]["outerwear"]
        if packed_outerwear is not None:
            i_g.generateOuterwear(userWardrobe, recommendation["primary_outfit"]["packed_outfit"], "packed_outfit.png")
        attachmentImages.append("packed_outfit.png")

    #image = Image.open("primary_outfit.png")
    send_email.sendEmail(userEmail, userEmail, attachmentImages)
    #image.show()

    

    
    

main()

