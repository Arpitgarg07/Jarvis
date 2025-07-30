import pyttsx3
import speech_recognition as sr
from win10toast import ToastNotifier
import time
import os

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

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

def remindme():
        toaster = ToastNotifier()
        Speak("what is the tittle of reminder sir!")
        Toasttitle = TakeCommand().lower()
        Speak("What should i remind sir!")
        msg = TakeCommand().lower()
        minutes = float(input("How Many Minutes: "))
        seconds = minutes * 60
        print("\nRemainder Set Successfully! \n")
        Speak("Reminder set Succesfully!")
        time.sleep(seconds)
        os.startfile("jarvisremind.mp3")
        toaster.show_toast(Toasttitle, msg, duration=10, threaded=True)
        while toaster.notification_active:
            time.sleep(0.1)
remindme()








