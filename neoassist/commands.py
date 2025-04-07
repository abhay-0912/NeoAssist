import subprocess
import os
from termcolor import colored
from .voice import speak
from .logger import logger
from serpapi import GoogleSearch
from .config import SERPAPI_KEY
import webbrowser

def web_search(query):
    try:
        if not SERPAPI_KEY:
            speak("Search API key not configured.")
            return

        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_KEY
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        top_result = results.get("organic_results", [{}])[0]
        title = top_result.get("title", "No title found.")
        link = top_result.get("link", "No link found.")

        speak(f"Top result: {title}")
        print(colored(f"Top result: {title}\n{link}", "cyan"))

    except Exception as e:
        speak("Failed to search.")
        print(colored(f"Error: {e}", "red"))


COMMANDS = [
    "open notepad",
    "open calculator",
    "open chrome",
    "shutdown",
    "restart",
    "logout",
    "read emails",
    "send email",
    "set reminder",
    "send whatsapp",
    "record screen",
    "record voice",
    "summarize email"
]

def suggest_command(user_input):
    import difflib
    closest_matches = difflib.get_close_matches(user_input, COMMANDS, n=1, cutoff=0.6)
    if closest_matches:
        suggestion = closest_matches[0]
        speak(f"Did you mean: {suggestion}?")
        print(colored(f"Did you mean: '{suggestion}'?", "yellow"))

def open_application(app_name):
    try:
        if app_name.lower() == "notepad":
            subprocess.run("notepad.exe")
        elif app_name.lower() == "calculator":
            subprocess.run("calc.exe")
        elif app_name.lower() == "chrome":
            subprocess.run("start chrome", shell=True)
        else:
            speak(f"Application {app_name} not supported yet.")
            print(colored(f"Application '{app_name}' not supported yet.", "red"))
            logger.warning(f"Unsupported application: {app_name}")
        logger.info(f"Opened application: {app_name}")
    except Exception as e:
        logger.error(f"Error opening application {app_name}: {e}")

def control_system(command):
    try:
        if command == "shutdown":
            os.system("shutdown /s /t 10")
        elif command == "restart":
            os.system("shutdown /r /t 10")
        elif command == "logout":
            os.system("shutdown -l")
        else:
            speak("Unknown system command.")
            print(colored("Unknown system command.", "red"))
            logger.warning(f"Unknown system command: {command}")
        logger.info(f"System control command executed: {command}")
    except Exception as e:
        logger.error(f"Error executing system command {command}: {e}")

def process_command(command):
    """
    Process the given command and execute the appropriate action.
    """
    if command == "hello":
        print("👋 Hello! How can I assist you?")
    elif command == "time":
        from datetime import datetime
        current_time = datetime.now().strftime("%H:%M:%S")
        print(f"⏰ The current time is {current_time}.")
    elif command.startswith("search for"):
        # Extract the search query and open it in the browser
        query = command.replace("search for", "").strip()
        if query:
            print(f"🔍 Searching for: {query}")
            webbrowser.open(f"https://www.google.com/search?q={query}")
        else:
            print("🤔 Please specify what you want to search for.")
    else:
        print(f"🤔 Sorry, I don't understand the command: {command}")
