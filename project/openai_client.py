import os
from openai import OpenAI

# Używa klucza z .env
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
