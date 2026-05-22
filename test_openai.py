from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Read API key
api_key = os.getenv("OPENAI_API_KEY")

# Create client
client = OpenAI(api_key=api_key)

# Send request
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role": "user",
            "content": "Say hello in German."
        }
    ]
)

# Print response
print(response.choices[0].message.content)