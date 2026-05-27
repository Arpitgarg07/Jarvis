"""
features/communication/sendemail.py
─────────────────────────────────────
Email sending via Gmail SMTP.
Credentials loaded from .env — never hardcoded.
"""

import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from core.voice import Speak

load_dotenv()

# Add recipient name → email mappings here
RECIPIENT_MAPPING = {
    "example": "example@gmail.com",
    # "mom": "mom@gmail.com",
}


def send_email(recipient_email: str, subject: str, content: str) -> None:
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        Speak("Email credentials not configured in .env file.")
        return

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(content)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully.")
        Speak("Email sent successfully.")
    except Exception as e:
        print(f"Email failed: {e}")
        Speak("Sorry, email could not be sent.")