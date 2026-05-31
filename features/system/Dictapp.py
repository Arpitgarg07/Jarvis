"""
features/system/Dictapp.py
───────────────────────────
System control functions: brightness, screenshots, window management.
Paths loaded from .env — no hardcoded contributor paths.
"""

import os
import pyautogui
import webbrowser
from time import sleep
from dotenv import load_dotenv
from core.voice import Speak, TakeCommand

load_dotenv()


# ── Screenshot ───────────────────────────────────────
def take_screenshot() -> None:
    import pyautogui
    from datetime import datetime
    path = os.path.expanduser("~/Pictures")
    os.makedirs(path, exist_ok=True)
    filename = f"jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    full = os.path.join(path, filename)
    pyautogui.screenshot(full)
    Speak(f"Screenshot saved.")
    print(f"Saved: {full}")


# ── Window Management ─────────────────────────────────
def minimize_window() -> None:
    pyautogui.hotkey('win', 'down')

def maximize_window() -> None:
    pyautogui.hotkey('win', 'up')

def close_window() -> None:
    Speak("Window closed.")
    pyautogui.hotkey('Alt', 'f4')

def go_to_home_screen() -> None:
    Speak("You are on the home screen.")
    pyautogui.hotkey('win', 'd')

# def lock_pc() -> None:
#     Speak("PC is locked.")
#     pyautogui.hotkey('win', 'l')

def lock_pc() -> None:
    Speak("Locking your PC.")
    import subprocess
    subprocess.run("rundll32.exe user32.dll,LockWorkStation")

def open_search() -> None:
    pyautogui.hotkey('win', 's')

def reload_page() -> None:
    pyautogui.hotkey('ctrl', 'r')

def switchtab() -> None:
    pyautogui.hotkey('Alt', 'Tab')

def pin_screen() -> None:
    Speak("Done sir.")
    pyautogui.hotkey('win', 'ctrl', 't')


# ── Brightness ────────────────────────────────────────
def set_brightness(percentage: int) -> None:
    try:
        import wmi
        wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(percentage, 0)
    except Exception as e:
        print(f"Brightness control failed: {e}")

def adjust_brightness(query) -> None:
    import re
    numbers = re.findall(r'\d+', query)
    if numbers:
        level = int(numbers[0])
        level = max(0, min(100, level))
    else:
        Speak("What brightness level? Say a number between 0 and 100.")
        resp = TakeCommand()
        nums = re.findall(r'\d+', resp)
        level = int(nums[0]) if nums else 50

    try:
        import wmi
        wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(level, 0)
        Speak(f"Brightness set to {level} percent.")
    except Exception:
        Speak("Could not change brightness. Make sure you're on a laptop.")


# ── Close Tabs ────────────────────────────────────────
def closeappweb(count: int = 1) -> None:
    Speak("Closing.")
    for _ in range(count):
        pyautogui.hotkey("ctrl", "w")
        sleep(0.5)
    Speak(f"{count} tab(s) closed.")


# ── Click Photo ───────────────────────────────────────
def click_photo() -> None:
    pyautogui.press("super")
    pyautogui.typewrite("camera")
    pyautogui.press("enter")
    sleep(1)
    Speak("Smile!")
    pyautogui.press("enter")
    Speak("Photo captured. You look great.")
    pyautogui.hotkey('Alt', 'f4')