import os
import subprocess
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import datetime
import speech_recognition as sr
import openai
import threading
import pyautogui
import cv2
import numpy as np
import pyaudio
import wave
from twilio.rest import Client

# OpenAI API Key
OPENAI_API_KEY = "your_openai_api_key"
openai.api_key = OPENAI_API_KEY

# Twilio API Credentials
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+your_twilio_number"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_whatsapp_message(to_number, message):
    try:
        message = client.messages.create(
            from_=TWILIO_WHATSAPP_NUMBER,
            body=message,
            to=f"whatsapp:{to_number}"
        )
        print(f"WhatsApp message sent successfully! Message SID: {message.sid}")
    except Exception as e:
        print("Error sending WhatsApp message:", e)

def open_application(app_name):
    if app_name.lower() == "notepad":
        subprocess.run("notepad.exe")
    elif app_name.lower() == "calculator":
        subprocess.run("calc.exe")
    elif app_name.lower() == "chrome":
        subprocess.run("start chrome", shell=True)
    else:
        print(f"Application '{app_name}' not supported yet.")

def control_system(command):
    if command == "shutdown":
        os.system("shutdown /s /t 10")  # Shutdown in 10 seconds
    elif command == "restart":
        os.system("shutdown /r /t 10")  # Restart in 10 seconds
    elif command == "logout":
        os.system("shutdown -l")
    else:
        print("Unknown system command.")

def summarize_email(body):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize this email: {body}",
        max_tokens=50
    )
    return response.choices[0].text.strip()

def read_emails():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("your_email@gmail.com", "your_password")
        mail.select("inbox")
        _, search_data = mail.search(None, "UNSEEN")
        email_ids = search_data[0].split()
        
        for num in email_ids[-5:]:  # Read last 5 unread emails
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            body = msg.get_payload(decode=True).decode(errors="ignore")
            summary = summarize_email(body)
            print(f"From: {msg['from']}, Subject: {msg['subject']}, Summary: {summary}")
        
        mail.logout()
    except Exception as e:
        print("Error reading emails:", e)

def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = "your_email@gmail.com"
        msg["To"] = to_email
        
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("your_email@gmail.com", "your_password")
        server.sendmail("your_email@gmail.com", to_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Error sending email:", e)

def set_reminder(task, time):
    reminders.append((task, time))
    print(f"Reminder set: {task} at {time}")

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")
    for task, time in reminders:
        if time == now:
            print(f"Reminder: {task}")

def recognize_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for a command...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio.")
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
    return ""

def continuous_listening():
    while True:
        command = recognize_voice()
        if command:
            process_command(command)

def auto_schedule_meeting(title, time):
    print(f"Auto-scheduling meeting: {title} at {time}")
    reminders.append((title, time))

def record_screen(output_filename="screen_record.avi", duration=10):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_filename, fourcc, 20.0, screen_size)
    
    for _ in range(20 * duration):  # Capture at 20 FPS for 'duration' seconds
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
    
    out.release()
    print(f"Screen recording saved as {output_filename}")

def record_audio(output_filename="audio_record.wav", duration=10):
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16
    channels = 1
    rate = 44100  # Sample rate
    p = pyaudio.PyAudio()
    
    stream = p.open(format=format, channels=channels,
                    rate=rate, input=True,
                    frames_per_buffer=chunk)
    print("Recording Audio...")
    frames = []
    
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    print(f"Audio recording saved as {output_filename}")

def process_command(user_input):
    if user_input.startswith("send whatsapp"):
        _, number, message = user_input.split(" ", 2)
        send_whatsapp_message(number, message)
    elif user_input.startswith("open "):
        app_name = user_input[5:]
        open_application(app_name)
    elif user_input in ["shutdown", "restart", "logout"]:
        control_system(user_input)
    elif user_input == "read emails":
        read_emails()
    elif user_input.startswith("record screen"):
        record_screen()
    elif user_input.startswith("record audio"):
        record_audio()
    else:
        print("Command not recognized.")
