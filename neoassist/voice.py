import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed
engine.setProperty('volume', 1)  # Volume

def speak(text):
    print(f"🗣️ NeoAssist: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"⚠️ Error in text-to-speech: {e}")