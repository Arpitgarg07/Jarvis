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
from core.voice import Speak

load_dotenv()


# ── Screenshot ───────────────────────────────────────
def take_screenshot() -> None:
    save_path = os.getenv("SCREENSHOT_PATH", os.path.expanduser("~/Pictures"))
    os.makedirs(save_path, exist_ok=True)
    filename = "screenshot.png"
    full_path = os.path.join(save_path, filename)
    screenshot = pyautogui.screenshot()
    screenshot.save(full_path)
    Speak("Screenshot saved.")
    print(f"Screenshot saved: {full_path}")


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

def lock_pc() -> None:
    Speak("PC is locked.")
    pyautogui.hotkey('win', 'l')

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

def adjust_brightness(level: str) -> None:
    levels = {
        "full": 100, "level 10": 100,
        "level 9": 90, "level 8": 80, "level 7": 70,
        "level 6": 60, "medium": 50, "level 5": 50,
        "level 4": 40, "level 3": 30, "level 2": 20,
        "level 1": 10, "low": 0, "level 0": 0,
    }
    for key, val in levels.items():
        if key in level:
            set_brightness(val)
            print(f"Brightness set to {val}%")
            return
    print("Brightness level not recognised.")


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