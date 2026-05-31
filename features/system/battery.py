from win10toast import ToastNotifier
import time
import psutil

from core.voice import Speak, TakeCommand

def battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    Speak(f"sir our system have {percentage} percent battery")
    if percentage >= 75:
        Speak("we have enough power to continue work.")
    elif percentage >= 40 and percentage <= 75:
        Speak("Battery is not more!,you should connect to Power source")
    elif percentage >= 15 and percentage <= 30:
        Speak("Battery running low, you should connect to power source")
    elif percentage >= 15:
        Speak("Batterysaver is running on, you must connect to power source")

def check_battery():
    toaster = ToastNotifier()
    while True:
        battery = psutil.sensors_battery()
        if battery.percent == 100 and not battery.power_plugged:
            toaster.show_toast("Battery Alert", "Battery is fully charged!", duration=10)
        time.sleep(300)  # Check the battery level every 60 seconds
