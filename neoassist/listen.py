import speech_recognition as sr
from .voice import speak

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=10)
    try:
        command = recognizer.recognize_google(audio)
        print(f"🧠 You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
    except sr.RequestError as e:
        speak("Sorry, I couldn't reach the speech recognition service.")
        print(f"⚠️ Speech recognition error: {e}")
    return ""

# Rename `recognize_speech` to `listen` for consistency
listen = recognize_speech
