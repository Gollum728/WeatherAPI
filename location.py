from dotenv import load_dotenv # Used to get data from the .env file
import os
import requests
import json
from datetime import datetime, timedelta

load_dotenv()

LOCATION_KEY = os.getenv("LOCATION_API_KEY")
url = "http://ip-api.com/json"

def getLocation():
    with open("config.json", "r") as file:
        data = json.load(file)
        if determineHoliday(data):
            return data["location_override"]
        
    response = requests.get(url)
    if response.status_code == 200:
        jsonData = response.json()
        print(jsonData)
        userCity = jsonData["city"]
        return userCity


def determineHoliday(data):
    if data["location_override"] is not None:
        tomorrowDate = (datetime.now() + timedelta(days=1)).date()
        overrideStart = datetime.strptime(data["override_start"], "%Y-%m-%d").date()
        overrideUntil = datetime.strptime(data["override_until"], "%Y-%m-%d").date()
        if overrideStart <= tomorrowDate <= overrideUntil:
            return True
        return False

