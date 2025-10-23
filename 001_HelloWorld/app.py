import os
from dotenv import load_dotenv
from google import genai

# Load variables from .env file
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="teach me generative ai",
)

print(response.text)
