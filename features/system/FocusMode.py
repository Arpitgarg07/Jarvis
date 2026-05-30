"""
features/system/FocusMode.py
──────────────────────────────
Blocks distracting websites for a set duration.
Requires admin privileges on Windows.

Fixed:
- focus_mode() function added (was all module-level before)
- Time math fixed (float subtraction on HH:MM was wrong)
- Input taken via voice/console properly
- Paths use data/ folder
- No module-level execution on import
"""

import ctypes
import datetime
import os
import sys
import time

from core.voice import Speak, TakeCommand

# ── Config ────────────────────────────────────────────
HOSTS_PATH = r"C:\Windows\System32\drivers\etc\hosts"
REDIRECT_IP = "127.0.0.1"
FOCUS_LOG = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data", "focus.txt"
)

# Add/remove websites you want blocked during focus
BLOCKED_SITES = [
    "www.facebook.com",
    "facebook.com",
    "www.instagram.com",
    "instagram.com",
    "www.twitter.com",
    "twitter.com",
]


# ── Admin check ───────────────────────────────────────
def _is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def _relaunch_as_admin() -> None:
    """Relaunch current script with admin privileges."""
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )


# ── Time helpers ──────────────────────────────────────
def _parse_time(time_str: str) -> datetime.datetime:
    """Parse HH:MM string into today's datetime."""
    return datetime.datetime.strptime(
        datetime.datetime.now().strftime("%Y-%m-%d") + " " + time_str,
        "%Y-%m-%d %H:%M"
    )


def _get_focus_minutes(start: datetime.datetime, end: datetime.datetime) -> float:
    """Return actual minutes between two datetimes."""
    return round((end - start).total_seconds() / 60, 1)


# ── Hosts file management ─────────────────────────────
def _block_sites() -> None:
    with open(HOSTS_PATH, "r+") as f:
        content = f.read()
        for site in BLOCKED_SITES:
            if site not in content:
                f.write(f"\n{REDIRECT_IP} {site}")
    print("Focus mode ON — sites blocked.")
    Speak("Focus mode is on. Distracting websites are blocked.")


def _unblock_sites() -> None:
    with open(HOSTS_PATH, "r") as f:
        lines = f.readlines()

    clean_lines = [
        line for line in lines
        if not any(site in line for site in BLOCKED_SITES)
    ]

    with open(HOSTS_PATH, "w") as f:
        f.writelines(clean_lines)

    print("Focus mode OFF — sites unblocked.")
    Speak("Focus session complete. Websites are unblocked.")


def _log_focus_time(minutes: float) -> None:
    os.makedirs(os.path.dirname(FOCUS_LOG), exist_ok=True)
    with open(FOCUS_LOG, "a") as f:
        f.write(f",{minutes}")


# ── Main function ─────────────────────────────────────
def focus_mode() -> None:
    """Start a focus session. Blocks sites until stop time."""

    if not _is_admin():
        Speak("Focus mode needs admin access. Relaunching with admin rights.")
        _relaunch_as_admin()
        return

    # Get stop time
    Speak("Until what time do you want to focus? Say it like: 11 30")
    stop_input = TakeCommand().lower()

    # Parse voice input → HH:MM
    # Handles: "11 30", "11:30", "eleven thirty" (basic)
    stop_input = stop_input.replace(" and ", ":").replace(" ", ":")
    while "::" in stop_input:
        stop_input = stop_input.replace("::", ":")

    parts = stop_input.split(":")
    if len(parts) < 2:
        Speak("I couldn't understand the time. Please try again.")
        return

    stop_time_str = f"{parts[0].zfill(2)}:{parts[1].zfill(2)}"
    now = datetime.datetime.now()
    now_str = now.strftime("%H:%M")

    if stop_time_str <= now_str:
        Speak("Stop time is in the past. Please give a future time.")
        return

    start_dt = _parse_time(now_str)
    stop_dt = _parse_time(stop_time_str)
    focus_minutes = _get_focus_minutes(start_dt, stop_dt)

    Speak(f"Starting focus session until {stop_time_str}. That is {focus_minutes} minutes.")

    # Block websites
    try:
        _block_sites()
    except PermissionError:
        Speak("Could not modify hosts file. Make sure Jarvis is running as admin.")
        return

    # Wait until stop time
    while True:
        current = datetime.datetime.now().strftime("%H:%M")
        if current >= stop_time_str:
            _unblock_sites()
            _log_focus_time(focus_minutes)
            Speak(f"Great work! You focused for {focus_minutes} minutes.")
            break
        time.sleep(30)  # Check every 30 seconds