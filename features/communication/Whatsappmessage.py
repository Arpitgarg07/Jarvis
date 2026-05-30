import os
import pyautogui
import webbrowser
import wmi
from time import sleep
import time
import pynput
from pynput.mouse import Button, Controller
from pynput import mouse

from core.voice import Speak, TakeCommand

phone_book = {
    "arpit garg": "6377181470",
    # ADD MORE CONTACTS.
}


def sendwhatsapp():
    query = TakeCommand().lower()
    message = phone_book
    pyautogui.hotkey('win', 's')
    pyautogui.sleep(1)
    pyautogui.typewrite("whatsapp")
    pyautogui.sleep(1)
    pyautogui.press("enter")
    pyautogui.sleep(2)
    Speak("Whom do you want to Message")
    pyautogui.typewrite(phone_book)
    pyautogui.sleep(2)
    pyautogui.moveTo(230,205)
    pyautogui.click()
    pyautogui.sleep(1)
    Speak("what is the Meassage...")
    pyautogui.typewrite("query")
    pyautogui.press("enter")
    Speak("Message send, Sir!")
    pyautogui.sleep(1)
    pyautogui.hotkey('alt', 'f4')
