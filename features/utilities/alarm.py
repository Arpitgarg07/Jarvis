"""
features/utilities/alarm.py
─────────────────────────────
Alarm system with proper time parsing and comparison.

Fixed:
- set_alarm() function added (called from Jarvismain)
- No module-level file reads (ran at import before = bug)
- Time comparison fixed (was string concat, not time math)
- Duplicate Speak removed, uses core.voice
- Paths fixed to data/ folder
"""

import datetime
import os
import time as time_module

from core.voice import Speak

ALARM_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "Alarmtext.txt"
)
ALARM_SOUND = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "assets", "media", "notification.mp3"
)


def set_alarm(alarm_input: str) -> None:
    """
    Parse alarm time from voice input and start ringing loop.
    Accepts formats like:
      - "10 and 30 and 00"  → 10:30:00
      - "10:30:00"          → 10:30:00
      - "10 30"             → 10:30:00
    """
    # Clean up voice input artifacts
    cleaned = (alarm_input
               .replace("jarvis", "")
               .replace("set an alarm", "")
               .replace(" and ", ":")
               .replace(" ", ":")
               .strip())

    # Remove double colons if any
    while "::" in cleaned:
        cleaned = cleaned.replace("::", ":")

    # Pad to HH:MM:SS if needed
    parts = cleaned.split(":")
    if len(parts) == 2:
        cleaned = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:00"
    elif len(parts) == 3:
        cleaned = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}:{parts[2].zfill(2)}"
    else:
        Speak("I couldn't understand the alarm time. Please say it like: 10 and 30.")
        return

    print(f"Alarm set for: {cleaned}")
    Speak(f"Alarm set for {cleaned}.")
    _ring(cleaned)


def _ring(alarm_time: str) -> None:
    """Wait until current time matches alarm_time then ring."""
    Speak("Alarm is active. I'll ring at the set time.")

    while True:
        current = datetime.datetime.now().strftime("%H:%M:%S")

        if current == alarm_time:
            Speak("Alarm ringing sir! Wake up!")
            _play_sound()
            break

        # Stop checking 1 minute after alarm time passed
        try:
            alarm_dt = datetime.datetime.strptime(alarm_time, "%H:%M:%S")
            now_dt = datetime.datetime.strptime(current, "%H:%M:%S")
            diff = (now_dt - alarm_dt).total_seconds()
            if diff > 60:
                print("Alarm time passed.")
                break
        except ValueError:
            break

        time_module.sleep(1)  # Check every second


def _play_sound() -> None:
    """Play alarm sound if available."""
    try:
        from pygame import mixer
        mixer.init()
        mixer.music.load(ALARM_SOUND)
        mixer.music.play()
        time_module.sleep(10)
        mixer.music.stop()
    except Exception as e:
        print(f"Could not play alarm sound: {e}")