from google import genai
from dotenv import load_dotenv # Used to get data from the .env file
import os
import json
import GoogleCalendar

load_dotenv()


CALENDAR_KEY = os.getenv("CALENDAR_API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
client = genai.Client(api_key = LLM_KEY)



def generateLLMResponse(weather, temperature, location, clothes):
    jsonFormat = """Return your answer as valid JSON in the following format:
    {
  "primary_outfit": {
    "top": "",
    "bottom": "",
    "outwear" : "",
    "packedClothes" : [],
    "confidence": 0
  },
  "backup_outfit": {
    "top": "",
    "bottom": "",
    "outwear" : "",
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
