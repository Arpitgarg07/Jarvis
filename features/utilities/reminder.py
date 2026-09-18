import time
import os
from plyer import notification
from core.voice import Speak, TakeCommand


def remindme():
    Speak("What is the title of reminder sir!")
    Toasttitle = TakeCommand().lower()
    Speak("What should I remind you about?")
    msg = TakeCommand().lower()
    Speak("In how many minutes?")
    minutes = float(input("How Many Minutes: "))
    seconds = minutes * 60
    print("\nReminder Set Successfully!\n")
    Speak("Reminder set successfully!")
    time.sleep(seconds)
    notification.notify(
        title=Toasttitle,
        message=msg,
        timeout=10,
    )
    Speak("Reminder time is up sir!")