import os
import time
import webbrowser
from time import sleep

import pyautogui
import pynput
import pyttsx3
import speech_recognition as sr
import wmi
from pynput import mouse
from pynput.mouse import Button, Controller


def TakeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 200
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language="en-in")
        print(f"Master said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
rate = engine.setProperty("rate", 185)


def Speak(audio):
    engine.say(audio)
    engine.runAndWait()


phone_book = {
    "Name": "PHONE_NUMBER",
    # ADD MORE CONTACTS.
}


def sendwhatsapp():
    query = TakeCommand().lower()
    message = phone_book
    pyautogui.hotkey("win", "s")
    pyautogui.sleep(1)
    pyautogui.typewrite("whatsapp")
    pyautogui.sleep(1)
    pyautogui.press("enter")
    pyautogui.sleep(2)
    Speak("Whom do you want to Message")
    pyautogui.typewrite(phone_book)
    pyautogui.sleep(2)
    pyautogui.moveTo(230, 205)
    pyautogui.click()
    pyautogui.sleep(1)
    Speak("what is the Meassage...")
    pyautogui.typewrite("query")
    pyautogui.press("enter")
    Speak("Message send, Sir!")
    pyautogui.sleep(1)
    pyautogui.hotkey("alt", "f4")
