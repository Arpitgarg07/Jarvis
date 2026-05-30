import pyjokes
from core.voice import Speak

def jokes():
    My_joke = pyjokes.get_joke(language="en", category="neutral")
    print(My_joke)
    Speak(My_joke)
