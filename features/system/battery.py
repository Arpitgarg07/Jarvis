import time
import psutil
from plyer import notification

from core.voice import Speak, TakeCommand

def battery():
    battery = psutil.sensors_battery()
    percentage = battery.percent
    plugged = battery.power_plugged

    status = "charging" if plugged else "not charging"
    Speak(f"Battery is at {percentage} percent and is currently {status}.")

    if plugged and percentage >= 99:
        Speak("Battery is fully charged. You can unplug the charger.")
    elif percentage >= 75:
        Speak("Battery level is good. No need to worry.")
    elif percentage >= 40:
        Speak("Battery is at medium level. Consider plugging in soon.")
    elif percentage >= 15:
        Speak("Battery is running low. Please connect to a power source.")
    else:
        Speak("Critical battery level! Connect to power immediately.")

def check_battery():
    while True:
        batt = psutil.sensors_battery()
        if batt.percent == 100 and not batt.power_plugged:
            notification.notify(
                title="Battery Alert",
                message="Battery is fully charged!",
                timeout=10,
            )
        time.sleep(300)  # Check the battery level every 60 seconds
