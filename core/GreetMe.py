import pyttsx3 
import datetime

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

# *Greet when it started.
def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<=12:
        Speak("Good Morning, Sir.")
    elif hour >= 12 and hour<=18:
        Speak("Good Afternoon, Sir.")   
    else:
        Speak("Good Evening, Master arpit.")

    Speak("I am Jarvis. How can I help you?")  





