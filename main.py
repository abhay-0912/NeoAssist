# NeoAssist - A personal assistant powered by AI
from neoassist.listen import listen
from neoassist.voice import speak
from neoassist.commands import process_command
from neoassist.logger import logger

def main():
    print("🚀 NeoAssist is starting...")
    logger.info("NeoAssist started")
    
    while True:
        speak("How can I help you?")
        command = listen()
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
