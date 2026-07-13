import smtplib
import ssl
from getpass import getpass
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_APP_KEY")

def sendEmail(sender, receiver):
    msg = EmailMessage()
    msg["to"] = receiver
    msg["from"] = sender
    msg["subject"] = "Outfit Picture"
    msg.set_content("This is a picture of the day's outfit")
    imageFile = Path("outfit.png")
    with open(imageFile, "rb") as image:
        msg.add_attachment(
            image.read(),
            maintype = "image",
            subtype = "png",
            filename = image.name,
        )

    send(msg, sender)

def send(msg, sender_email):
    smtp_server = "smtp.gmail.com"
    port = 465
    password = EMAIL_PASSWORD
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        smtp_server, port, context=context
    ) as server:
        server.login(sender_email, password)
        server.send_message(msg)


sendEmail("raghavj8989@gmail.com", "raghavj8989@gmail.com")