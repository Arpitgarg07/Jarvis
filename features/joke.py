import pyjokes
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

def jokes():
    My_joke = pyjokes.get_joke(language="en", category="neutral")
    print(My_joke)
    Speak(My_joke)
