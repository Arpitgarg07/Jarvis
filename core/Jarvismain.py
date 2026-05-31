"""
core/Jarvismain.py
───────────────────
Main Jarvis assistant loop.

Clean rewrite:
- No duplicate Speak / TakeCommand (imported from core.voice)
- No hardcoded credentials (all from .env)
- Command map instead of 50+ if/elif chain
- Module-level side effects removed
"""

import datetime
import os
import random
import subprocess
import sys
import time
import webbrowser

import pyautogui
import requests
import speedtest
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from plyer import notification
from pygame import mixer

from core.voice import TakeCommand, Speak
from core.GreetMe import greetMe

# ── Feature imports ───────────────────────────────────
from features.communication.Whatsapp import sendMessage
from features.communication.Whatsappmessage import sendwhatsapp
from features.communication.sendemail import send_email, RECIPIENT_MAPPING
from features.entertainment.NewsRead import latestnews
from features.entertainment.joke import jokes
from features.entertainment.game import game_play
from features.search.SearchNow import searchGoogle, searchyoutube, searchwikipedia
from features.system.battery import battery
from features.system.Dictapp import (
    take_screenshot, click_photo, minimize_window, maximize_window,
    close_window, lock_pc, go_to_home_screen, open_search,
    reload_page, switchtab, pin_screen, closeappweb, adjust_brightness,
)
from features.system.keyboard import volumeup, volumedown
from features.system.FocusMode import focus_mode
from features.utilities.Calculatenumbers import Calc
from features.utilities.FocusGraph import focus_graph
from features.utilities.Location import My_Location
from features.utilities.Translator import translategl
from features.utilities.alarm import set_alarm
from features.utilities.reminder import remindme
from features.utilities.sendcall import send_call
from features.utilities.task_manager import (
    add_task, summary_text, mark_completed, set_priority,
)


# ── Config ────────────────────────────────────────────
CHROME_PATH = os.getenv("CHROME_PATH", "C:/Program Files/Google/Chrome/Application/chrome.exe")
CONTACT_DICT = {
    "raja": "+916377181470",
    "anshika": "+919351062165",
    "mummy": "+918619456246",
    "papa": "+917014832024",
    "kinshu": "+919351366529",
    "chacha": "+919694846502",
    "arpit": "+916375014040",
    "baba": "+918741890153"
}
GOODBYES = ["You are great!", "Thanks for using me!", "Nice meeting with you!"]

# ── Chrome browser setup ──────────────────────────────

# ── Sounds ────────────────────────────────────────────


# ══════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ══════════════════════════════════════════════════════

def cmd_greet(query):
    responses = {
        "hello": "Hello sir, how can I help you!",
        "hi": "Hello sir, how can I help you!",
        "hey": "Hey! What can I do for you?",
        "namaste": "Namaste, sir!",
        "ram ram": "Ram Ram, Master!",
        "good morning": "Good Morning Sir!",
        "good evening": "Good Evening Sir!",
        "good afternoon": "Good Afternoon Sir!",
        "how are you": "Perfect, sir!",
        "kaise ho": "I am good, thanks for asking!",
    }
    for key, reply in responses.items():
        if key in query:
            Speak(reply)
            return


def cmd_translate(query):
    query = query.replace("jarvis translate", "").replace("translate", "").strip()
    translategl(query)


def cmd_joke(_query):
    jokes()


def cmd_battery(_query):
    battery()


def cmd_remember(query):
    msg = query.replace("remember that", "").replace("jarvis", "").strip()
    with open("data/Remember.txt", "a") as f:
        f.write(msg + "\n")
    Speak(f"Got it. I'll remember: {msg}")


def cmd_recall(_query):
    try:
        with open("data/Remember.txt", "r") as f:
            content = f.read()
        Speak("You told me to " + content if content else "I don't have anything saved.")
    except FileNotFoundError:
        Speak("Nothing saved yet.")


def cmd_focus_mode(_query):
    focus_mode()


def cmd_focus_graph(_query):
    focus_graph()


def cmd_game(_query):
    game_play()


def cmd_play_playlist(_query):
    url = "https://www.youtube.com/watch?v=DbiRVNeZPnw&list=PLpmsNGoQrkhF1nNjDVXAcyVsNnLOdw_1h"
    Speak("Music playing...")
    webbrowser.get("chrome").open(url)


def cmd_coin_flip(_query):
    outcome = random.choice(["heads", "tails"])
    try:
        mixer.init()
        coin_sound = mixer.Sound("assets/media/coin.mp3")
        coin_sound.play()
    except Exception:
        pass
    Speak(f"The coin landed on {outcome}!")


def cmd_time(_query):
    t = datetime.datetime.now().strftime("%H:%M:%S")
    Speak(f"Sir, the time is {t}")


def cmd_alarm(query):
    Speak("What time should I set the alarm for?")
    alarm_time = input("Enter alarm time (HH and MM and SS): ")
    set_alarm(alarm_time)
    Speak("Alarm set.")


def cmd_remind(_query):
    remindme()


def cmd_add_task(query):
    urgent = "urgent" in query
    clean = (query.replace("jarvis", "")
                  .replace("add urgent task", "")
                  .replace("add task", "")
                  .strip())
    priority = "high" if urgent else "normal"
    deadline_text = None
    for kw in [" by ", " before ", " at ", " on "]:
        if kw in clean:
            parts = clean.split(kw, 1)
            clean = parts[0].strip()
            deadline_text = parts[1].strip()
            break
    if clean:
        t = add_task(clean, deadline_text, priority)
        Speak(f"Task added: {t['title']}")
    else:
        Speak("Please say the task name.")


def cmd_tasks_today(_query):
    Speak(summary_text("today"))


def cmd_tasks_week(_query):
    Speak(summary_text("week"))


def cmd_tasks_overdue(_query):
    Speak(summary_text("overdue"))


def cmd_mark_done(query):
    title = (query.replace("jarvis", "")
                  .replace("mark task completed", "")
                  .replace(":", "")
                  .strip())
    done = mark_completed(title)
    Speak(f"Marked done: {done['title']}" if done else "Task not found.")


def cmd_ip(_query):
    ip = requests.get("https://api.ipify.org").text
    Speak(f"Your IP address is {ip}")


def cmd_temperature(_query):
    try:
        city = "Jaipur"
        url = f"https://wttr.in/{city}?format=%t"
        response = requests.get(url, timeout=5)
        temp = response.text.strip()
        Speak(f"Current temperature in {city} is {temp}")
    except Exception:
        Speak("Could not fetch temperature right now.")

def cmd_calculate(query):
    query = (query.replace("calculate", "").replace("jarvis", "")
                  .replace("what is", "").replace("solve", "")
                  .replace("plus", "+").replace("minus", "-")
                  .replace("multiply", "*").replace("divided by", "/")
                  .replace("times", "*").strip())
    try:
        result = eval(query)
        Speak(f"The answer is {result}")
    except Exception:
        Speak("Sorry, I could not calculate that.")

def cmd_internet_speed(_query):
    Speak("Testing internet speed, please wait...")
    wifi = speedtest.Speedtest()
    upload = wifi.upload() / 1048576
    download = wifi.download() / 1048576
    Speak(f"Download speed is {download:.1f} Mbps and upload speed is {upload:.1f} Mbps")


def cmd_send_call(_query):
    send_call()


def cmd_search_google(query):
    query = query.replace("jarvis", "").replace("google search", "").replace("google", "").strip()
    searchGoogle(query)


def cmd_search_youtube(query):
    searchyoutube(query)


def cmd_search_wikipedia(query):
    searchwikipedia(query)


def cmd_news(_query):
    latestnews()


def cmd_location(_query):
    My_Location()


def cmd_whatsapp(query):
    if "whatsapp message" in query:
        sendwhatsapp()
    else:
        sendMessage(CONTACT_DICT)


def cmd_email(_query):
    Speak("Who do you want to email?")
    name = TakeCommand().lower()
    email_addr = RECIPIENT_MAPPING.get(name)
    if not email_addr:
        Speak("Recipient not found.")
        return
    Speak("What is the subject?")
    subject = TakeCommand()
    Speak("What is the message?")
    content = TakeCommand()
    send_email(email_addr, subject, content)


def cmd_screenshot(_query):
    take_screenshot()


def cmd_open_app(query):
    app = query.replace("open", "").replace("jarvis", "").strip()
    pyautogui.press("super")
    pyautogui.typewrite(app)
    pyautogui.sleep(1)
    pyautogui.press("enter")
    Speak(f"Launching {app}...")


def cmd_close(query):
    import subprocess
    app = (query.replace("close", "").replace("jarvis", "").strip())
    if app:
        subprocess.run(f"taskkill /f /im {app}.exe", shell=True)
        Speak(f"Closing {app}.")
    else:
        pyautogui.hotkey("alt", "f4")
        Speak("Closed.")

# def cmd_close(query):
#     closeappweb(query)


def cmd_volume_up(_query):
    volumeup()
    Speak("Volume up.")


def cmd_volume_down(_query):
    volumedown()
    Speak("Volume down.")


def cmd_minimize(_query):
    minimize_window()


def cmd_maximize(_query):
    maximize_window()


def cmd_close_window(_query):
    close_window()


def cmd_lock(_query):
    lock_pc()


def cmd_home(_query):
    go_to_home_screen()


def cmd_reload(_query):
    reload_page()


def cmd_switch_tab(_query):
    switchtab()


def cmd_pin_screen(_query):
    pin_screen()


def cmd_brightness(query):
    from features.system.Dictapp import adjust_brightness
    adjust_brightness(query)


def cmd_click_photo(_query):
    click_photo()


def cmd_open_search(_query):
    open_search()


def cmd_website(query):
    sites = {
        "stackoverflow": "stackoverflow.com",
        "amazon": "amazon.in",
        "flipkart": "flipkart.com",
        "meesho": "meesho.com",
        "myntra": "myntra.com",
        "speed test": "fast.com",
        "our channel": "https://www.youtube.com/channel/UCAi-EONczHNaAqr_Ff3HRsA",
    }
    for key, url in sites.items():
        if key in query:
            webbrowser.get("chrome").open(url)
            Speak(f"Opening {key}...")
            return


def cmd_youtube_control(query):
    controls = {
        "full screen": "f", "theater mode": "t", "mini player": "i",
        "pause": "k", "play": "k", "rewind": "j", "forward": "l",
        "mute": "m",
    }
    for key, hotkey in controls.items():
        if key in query:
            pyautogui.press(hotkey)
            Speak(f"{key} activated.")
            return


def cmd_change_password(_query):
    Speak("What is the new password?")
    new_pw = input("Enter new password: ")
    with open("data/password.txt", "w") as f:
        f.write(new_pw)
    Speak("Password updated.")


def cmd_shutdown(_query):
    Speak("Are you sure you want to shutdown?")
    confirm = TakeCommand().lower()
    if "yes" in confirm:
        Speak("Shutting down.")
        os.system("shutdown /s /t 1")


def cmd_exit(_query):
    Speak(random.choice(GOODBYES))
    sys.exit()


# ══════════════════════════════════════════════════════
#  COMMAND MAP  — keyword → handler function
#  Order matters: more specific keywords first
# ══════════════════════════════════════════════════════

COMMAND_MAP = [
    # Sleep / exit
    ("go to sleep",         lambda q: None),          # handled in loop
    ("exit",                cmd_exit),
    ("shutdown",            cmd_shutdown),

    # Greetings
    ("hello",               cmd_greet),
    ("hi ",                 cmd_greet),
    ("hey",                 cmd_greet),
    ("namaste",             cmd_greet),
    ("ram ram",             cmd_greet),
    ("good morning",        cmd_greet),
    ("good evening",        cmd_greet),
    ("good afternoon",      cmd_greet),
    ("how are you",         cmd_greet),
    ("kaise ho",            cmd_greet),

    # Utilities
    ("translate",           cmd_translate),
    ("joke",                cmd_joke),
    ("battery",             cmd_battery),
    ("remember that",       cmd_remember),
    ("what do you remember",cmd_recall),
    ("flip a coin",         cmd_coin_flip),
    ("coin flip",           cmd_coin_flip),
    ("toss",                cmd_coin_flip),
    ("time",                cmd_time),
    ("temperature",         cmd_temperature),
    ("calculate",           cmd_calculate),
    ("ip address",          cmd_ip),
    ("internet speed",      cmd_internet_speed),

    # Tasks
    ("add urgent task",     cmd_add_task),
    ("add task",            cmd_add_task),
    ("tasks today",         cmd_tasks_today),
    ("tasks this week",     cmd_tasks_week),
    ("overdue tasks",       cmd_tasks_overdue),
    ("mark task completed", cmd_mark_done),
    ("set an alarm",        cmd_alarm),
    ("remind me",           cmd_remind),

    # Focus
    ("focus mode",          cmd_focus_mode),
    ("show my focus",       cmd_focus_graph),

    # Entertainment
    ("open game",           cmd_game),
    ("play playlist",       cmd_play_playlist),
    ("news",                cmd_news),

    # Search
    ("google",              cmd_search_google),
    ("youtube search",      cmd_search_youtube),
    ("youtube",             cmd_search_youtube),
    ("wikipedia",           cmd_search_wikipedia),

    # Communication
    ("whatsapp message",    cmd_whatsapp),
    ("whatsapp",            cmd_whatsapp),
    ("write an email",      cmd_email),
    ("send call",           cmd_send_call),

    # Location
    ("my location",         cmd_location),
    ("where i am",          cmd_location),

    # YouTube controls
    ("full screen",         cmd_youtube_control),
    ("theater mode",        cmd_youtube_control),
    ("mini player",         cmd_youtube_control),
    ("rewind",              cmd_youtube_control),
    ("forward",             cmd_youtube_control),

    # Volume
    ("volume up",           cmd_volume_up),
    ("volume down",         cmd_volume_down),
    ("mute",                cmd_youtube_control),
    ("pause",               cmd_youtube_control),
    ("play",                cmd_youtube_control),

    # System
    ("screenshot",          cmd_screenshot),
    ("click photo",         cmd_click_photo),
    ("minimise",            cmd_minimize),
    ("minimize",            cmd_minimize),
    ("maximize",            cmd_maximize),
    ("maximise",            cmd_maximize),
    ("close window",        cmd_close_window),
    ("close tab",           cmd_close_window),
    ("lock",                cmd_lock),
    ("home",                cmd_home),
    ("reload",              cmd_reload),
    ("switch tab",          cmd_switch_tab),
    ("switch app",          cmd_switch_tab),
    ("pin screen",          cmd_pin_screen),
    ("brightness",          cmd_brightness),
    ("open search",         cmd_open_search),
    ("change password",     cmd_change_password),

    # Websites
    ("stackoverflow",       cmd_website),
    ("amazon",              cmd_website),
    ("flipkart",            cmd_website),
    ("meesho",              cmd_website),
    ("myntra",              cmd_website),
    ("speed test",          cmd_website),
    ("our channel",         cmd_website),

    # Open / close apps (generic — keep last)
    ("open",                cmd_open_app),
    ("close",               cmd_close),
]


def handle_command(query: str) -> bool:
    """Route query to the right handler. Returns True if handled."""
    for keyword, handler in COMMAND_MAP:
        if keyword in query:
            handler(query)
            return True
    Speak("I didn't understand that. Could you repeat?")
    return False


# ══════════════════════════════════════════════════════
#  MAIN LOOP
# ══════════════════════════════════════════════════════
def run():
    print("Jarvis is ready. Say 'wake up' to start.")
    webbrowser.register("chrome", None, 
                       webbrowser.BackgroundBrowser(CHROME_PATH))

    while True:
        try:
            query = TakeCommand().lower()
            if query == "none":
                continue

            if "wake up" in query or "start" in query or "break up" in query or "makeup" in query:
                greetMe()

                while True:
                    try:
                        query = TakeCommand().lower()
                        if query == "none":
                            continue
                        if "go to sleep" in query:
                            Speak("Ok sir, call me anytime.")
                            break
                        handle_command(query)
                    except Exception as e:
                        print(f"Command error: {e}")
                        Speak("Something went wrong, try again.")
                        continue  # crash nahi hoga, sunna jaari rahega

        except KeyboardInterrupt:
            Speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue

if __name__ == "__main__":
    run()