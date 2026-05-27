"""
features/utilities/Calculatenumbers.py
────────────────────────────────────────
WolframAlpha + basic math calculations.
API key loaded from .env — never hardcoded.
"""

import os
import wolframalpha
from dotenv import load_dotenv
from core.voice import Speak

load_dotenv()


def WolfRamAlpha(query: str) -> str | None:
    api_key = os.getenv("WOLFRAM_API_KEY")
    if not api_key:
        Speak("WolframAlpha API key not configured.")
        return None

    client = wolframalpha.Client(api_key)
    result = client.query(query)

    try:
        return next(result.results).text
    except Exception:
        Speak("The value is not answerable.")
        return None


def Calc(query: str) -> None:
    query = (query
             .replace("jarvis", "")
             .replace("multiply", "*")
             .replace("plus", "+")
             .replace("minus", "-")
             .replace("divide", "/")
             .strip())

    result = WolfRamAlpha(query)
    if result:
        print(result)
        Speak(result)