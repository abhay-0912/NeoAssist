import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "default_openai_key")
EMAIL = os.getenv("NEO_EMAIL", "default_email@example.com")
PASSWORD = os.getenv("NEO_PASSWORD", "default_password")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "default_sid")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "default_auth_token")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "default_whatsapp_number")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY", "default_serpapi_key")

# Ensure SERPAPI_KEY is defined
SERPAPI_KEY = "your_serpapi_key_here"  # Replace with your actual SERPAPI key
