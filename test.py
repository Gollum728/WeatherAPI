import requests
import os
from dotenv import load_dotenv # Used to get data from the .env file
from google import genai

load_dotenv()
API_KEY = os.getenv("API_KEY")
LLM_KEY = os.getenv("LLM_API_KEY")

client = genai.Client(api_key=LLM_KEY)

response = client.models.generate_content_stream( # Creates a stream
    model = "gemini-3.5-flash",
    contents = "Tell me a joke"
)

for chunk in response:
    print(chunk)
    print(chunk.text, end="")