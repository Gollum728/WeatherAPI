from google import genai
import google
from dotenv import load_dotenv # Used to get data from the .env file
import os
import json
import sys


load_dotenv()


CALENDAR_KEY = os.getenv("CALENDAR_API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")
client = genai.Client(api_key = LLM_KEY)



def generateLLMResponse(weather, location, clothes, events):
    jsonFormat = """Return your answer as valid JSON in the following format.

          If no outerwear is required, set "outerwear" to null. Otherwise, set it to the exact name of the outerwear item from the provided clothing list.

          If no additional outfit needs to be packed, set "packed_outfit" to null.

          If an additional outfit needs to be packed, "packed_outfit" must contain the complete outfit that should be packed. Use the exact names of clothing items from the provided clothing list.

          {
            "primary_outfit": {
              "top": "",
              "bottom": "",
              "outerwear": null,
              "packed_outfit": {
                "top": "",
                "bottom": "",
                "outerwear": null
              },
              "confidence": 0
            },
            "backup_outfit": {
              "top": "",
              "bottom": "",
              "outerwear": null,
              "packed_outfit": {
                "top": "",
                "bottom": "",
                "outerwear": null
              },
              "confidence": 0
            }
          }"""
    try:
      llmResponse = client.models.generate_content_stream(
          model = "gemini-3.5-flash",
          contents = f"Tomorrow I will be in {location}. Here is the weather tomorrow in {location} : {weather}. Here is a list of the clothes that I own : {clothes}. Here are the events that I have today {events}. Based on this, give me 2 outfit recommendations using the clothes that I have - 1 outfit that would suit the weather conditions and the events I have tomorrow perfectly, and 1 backup option. If necessary, I can pack a bag with another set of clothes if an event I have requires a change of clothes, but don't include multiple outfit changes - I can only take 1 bag with 1 outfit inside! The colour of the clothing should be considered when making a decision - both the top and bottom ideally shouldn't be the same unless required. Give me a confidence score out of 10 for both of these options. Don't add extra details about the clothes, only use the details that are provided. Return your response in a JSON format like this: {jsonFormat}. Return only the JSON object. Don't include markdown or any explanations!"
      )

      output = ""
      for chunks in llmResponse:
          output += chunks.text
      jsonOutput = json.loads(output)
      print(jsonOutput)
      return jsonOutput
    except google.genai.errors.ServerError:
      sys.exit("Server is experiencing high demand, please try later")