import pywhatkit
import pyttsx3
import speech_recognition as sr
import webbrowser
from bs4 import BeautifulSoup
from time import sleep
import os 
from datetime import timedelta
from datetime import datetime
import time
import pyautogui

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate",185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()


#^ For taking all commands and listen the user voices.
def TakeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 200
        audio = r.listen(source,0,4)

    try:
        print("Understanding...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"Master said: {query}\n")

    except Exception as e:
        print("Say that again please...") 
        return "None"
    return query

def sendMessage(contact_dict):

    strTime = int(datetime.now().strftime("%H"))
    update = int((datetime.now() + timedelta(minutes=2)).strftime("%M"))

    Speak("Who do you want to message?")
    contact_name = TakeCommand().lower()

    if contact_name in contact_dict:
        Speak("What's the message?")
        message = TakeCommand()
        contact_number = contact_dict[contact_name]
        pywhatkit.sendwhatmsg(contact_number, message, time_hour=strTime, time_min=update)
    
        Speak("Message delivered!")
        pyautogui.hotkey('Alt','f4')

    else:
        Speak("Sorry, I couldn't find the contact.")



