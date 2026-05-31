import pywhatkit
import webbrowser
from datetime import timedelta, datetime
import time
import os
import pyautogui

from core.voice import Speak, TakeCommand

def sendMessage(contact_dict):
    Speak("Who do you want to message?")
    contact_name = TakeCommand().lower()

    if contact_name not in contact_dict:
        Speak("Contact not found.")
        return

    Speak("What's the message?")
    message = TakeCommand()
    contact_number = contact_dict[contact_name]

    # WhatsApp Desktop app se seedha
    url = f"whatsapp://send?phone={contact_number}&text={message}"
    os.startfile(url)
    time.sleep(4)
    pyautogui.hotkey('enter')
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')
    Speak("Message sent!")