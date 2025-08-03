import os
import sys
import dotenv
from baml_client import b

dotenv.load_dotenv()

api_key = os.environ.get("NEBIUS_API_KEY")

text = "I want my money back now!"
themes = [
    {"title": "Technical support", "description": "The customer is calling for technical support"},
    {"title": "Billing", "description": "The customer is calling for billing issues"},
    {"title": "Refund", "description": "The customer is calling for a refund"},
]

result = b.TextClassification(text=text, themes=themes)

print(result.chosen_theme)
print(result.model_reasoning)