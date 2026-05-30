import time
import os
from win10toast import ToastNotifier
from core.voice import Speak, TakeCommand


def remindme():
    toaster = ToastNotifier()
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
    toaster.show_toast(Toasttitle, msg, duration=10, threaded=True)
    while toaster.notification_active():
        time.sleep(0.1)
    Speak("Reminder time is up sir!")