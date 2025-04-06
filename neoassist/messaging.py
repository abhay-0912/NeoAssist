from twilio.rest import Client
from termcolor import colored
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER
from .voice import speak
from .logger import logger

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number, message):
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=f"whatsapp:{to_number}"
        )
        speak("WhatsApp message sent successfully!")
        print(colored("WhatsApp message sent successfully!", "green"))
        logger.info(f"WhatsApp message sent to {to_number}")
    except Exception as e:
        logger.error(f"Error sending WhatsApp message: {e}")
        print(colored("Error sending WhatsApp message:", "red"), e)
        speak("Error sending WhatsApp message")
