import smtplib
import ssl
from getpass import getpass
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

EMAIL_PASSWORD = os.getenv("EMAIL_APP_KEY")

def sendEmail(sender, receiver, attachments):
    msg = EmailMessage()
    msg["to"] = receiver
    msg["from"] = sender
    msg["subject"] = "Outfit Picture"
    if len(attachments) == 1:
        content = """Here is your recommended outfit for today based on the weather and your calendar.
                    Your recommended outfit is attached below.
                    Have a great day!"""
    else:
        content = """Here are your recommended outfits for today based on the weather and your calendar.
                    The first image shows your primary outfit.
                    The second image shows the additional outfit recommended for you to pack for later in the day.
                    Have a great day!"""
        
    msg.set_content(content)
    for attachment in attachments:
        imageFile = Path(attachment)
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
