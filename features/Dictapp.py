import os
import pyautogui
import webbrowser
import pyttsx3
import wmi
import speech_recognition as sr
from time import sleep

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

#^ Adjusting brightness at fixed level.
def adjust_brightness():
    query = TakeCommand().lower()

    if "level 10" in query or "full" in query:
        set_brightness(100)
        print("Brightness at level 10")
    elif "level 9" in query:
        set_brightness(90)
        print("Brightness at level 9")
    elif "level 8" in query:
        set_brightness(80)
        print("Brightness at level 8")
    elif "level 7" in query:
        set_brightness(70)
        print("Brightness at level 7")
    elif "level 6" in query:
        set_brightness(60)
        print("Brightness increased 6")
    elif "level 5" in query or "medium" in query:
        set_brightness(50)
        print("Brightness at level 5")
    elif "level 4" in query:
        set_brightness(40)
        print("Brightness at level 4")
    elif "level 3" in query:
        set_brightness(30)
        print("Brightness at level 3")
    elif "level 2" in query:
        set_brightness(20)
        print("Brightness at level 2")
    elif "level 1" in query:
        set_brightness(10)
        print("Brightness at level 1")
    elif "level 0" in query or "low" in query or "decrease" in query:
        set_brightness(0)
        print("Brightness at level 0")

    else:
        print("Command not understanding...")

#* Keyboard Shortcuts
def minimize_window():
    pyautogui.hotkey('win', 'down')

def switchtab():
    pyautogui.hotkey('Alt', 'Tab')

# Function to capture a screenshot
def take_screenshot():
    screenshot = pyautogui.screenshot()
    save_path = r"C:\Users\gomti\OneDrive\Pictures\Screenshots"    #add the folder location of taking screenshot
    filename = "screenshot.png"
    screenshot.save(os.path.join(save_path, filename))
    Speak("Screenshot saved.")
    print(f"Screenshot saved as {os.path.join(save_path, filename)}")

def click_photo():
    pyautogui.press("super")
    pyautogui.typewrite("camera")
    pyautogui.press("enter")
    pyautogui.sleep(1)
    Speak("SMILE")
    pyautogui.press("enter")
    Speak("Your photo is captured, you looking Good.")
    pyautogui.hotkey('Alt','f4')

# Function to open search
def open_search():
    pyautogui.hotkey('win', 's')

# Function to pin screen
def pin_screen():
    Speak("Done Sir")
    pyautogui.hotkey('win', 'ctrl', 't')

# Function to close window
def close_window():
    Speak("window closed")
    pyautogui.hotkey('Alt','f4')

# Function to lock PC
def lock_pc():
    pyautogui.hotkey('win', 'l')
    Speak("PC is locked")

# Function to go to the home screen
def go_to_home_screen():
    Speak("You are on home screen now!")
    pyautogui.hotkey('win', 'd')

# Function to reload or refresh
def reload_page():
    pyautogui.hotkey('ctrl', 'r')

# Function to maximize the active window
def maximize_window():
    pyautogui.hotkey('win', 'up')
    
# Function to adjust brightness of your pc
def set_brightness(percentage):
    wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(percentage, 0)

def closeappweb(query):
    Speak("Closing sir")
    if "one tab" in query or "1 tab" in query:
        pyautogui.hotkey("ctrl","w")
    elif "two tab" in query or "2 tab " in query:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        Speak("All tabs closed")
    elif "3 tab" in query:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        Speak("All tabs closed")
    elif "4 tab" in query:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        Speak("All tabs closed")
    elif "5 tab" in query:
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        sleep(0.5)
        pyautogui.hotkey("ctrl","w")
        Speak("All tabs closed")
    



