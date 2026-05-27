"""
features/utilities/sendcall.py
────────────────────────────────
Twilio voice call integration.
Credentials loaded from .env — never hardcoded.
"""

import os
from dotenv import load_dotenv
from core.voice import Speak, TakeCommand

load_dotenv()


def send_call() -> None:
    sid = os.getenv("TWILIO_SID")
    token = os.getenv("TWILIO_TOKEN")
    from_number = os.getenv("TWILIO_NUMBER")

    if not all([sid, token, from_number]):
        Speak("Twilio credentials not configured in .env file.")
        return

    Speak("Who do you want to call? Please say the number.")
    to_number = TakeCommand()

    if to_number == "None":
        Speak("Could not understand the number.")
        return

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        call = client.calls.create(
            twiml='<Response><Say>Hello, this is Jarvis calling.</Say></Response>',
            from_=from_number,
            to=to_number
        )
        Speak(f"Call placed successfully.")
        print(f"Call SID: {call.sid}")
    except Exception as e:
        Speak("Call failed.")
        print(f"Twilio error: {e}")