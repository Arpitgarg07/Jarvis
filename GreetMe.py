"""
Lightweight, test-friendly GreetMe module.

Implements Speak and greetMe in a way that works well with unit tests:
- Initializes pyttsx3 engine inside functions so patched `pyttsx3.init`
  in tests captures calls.
- Uses this module's `datetime.datetime` so tests can patch it.
"""

import datetime

import pyttsx3


def Speak(audio: str) -> None:
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 185)
    engine.say(audio)
    engine.runAndWait()


def greetMe() -> None:
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        Speak("Good Morning, Sir.")
    elif 12 <= hour <= 18:
        Speak("Good Afternoon, Sir.")
    else:
        Speak("Good Evening, Master arpit.")
    Speak("I am Jarvis. How can I help you?")
