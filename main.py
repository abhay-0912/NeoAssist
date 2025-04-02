import os
import subprocess
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
import datetime
import speech_recognition as sr

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
            print(f"From: {msg['from']}, Subject: {msg['subject']}")
        
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

def main():
    global reminders
    reminders = []
    while True:
        check_reminders()
        user_input = input("NeoAssist > Type or say 'voice' to use voice commands: ").strip().lower()
        
        if user_input == "voice":
            user_input = recognize_voice()
        
        if user_input in ["exit", "quit"]:
            print("Exiting NeoAssist...")
            break
        elif user_input.startswith("open "):
            app_name = user_input[5:]
            open_application(app_name)
        elif user_input in ["shutdown", "restart", "logout"]:
            control_system(user_input)
        elif user_input == "read emails":
            read_emails()
        elif user_input.startswith("send email "):
            parts = user_input[11:].split(",")
            if len(parts) == 3:
                send_email(parts[0].strip(), parts[1].strip(), parts[2].strip())
            else:
                print("Invalid format. Use: send email recipient, subject, body")
        elif user_input.startswith("remind me "):
            parts = user_input[10:].split(" at ")
            if len(parts) == 2:
                set_reminder(parts[0].strip(), parts[1].strip())
            else:
                print("Invalid format. Use: remind me Task at HH:MM")
        else:
            print("Command not recognized.")

if __name__ == "__main__":
    main()
