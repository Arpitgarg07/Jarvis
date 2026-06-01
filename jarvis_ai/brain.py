"""
jarvis_ai/brain.py
───────────────────
Jarvis AI Brain — Multi-key Groq + Gemini Vision

Features:
- Multiple Groq API keys auto-rotation
- Fixed vision with proper screenshot handling
- Gemini 2.0 Flash for accurate screen reading
"""

import os
import json
import time
import base64
import requests
import subprocess
from io import BytesIO

import pyautogui
import uiautomation as auto
from dotenv import load_dotenv
from core.voice import Speak

load_dotenv()

# ══════════════════════════════════════════════════════
# MULTI-KEY GROQ ROTATION
# ══════════════════════════════════════════════════════

def _load_groq_keys() -> list:
    """Load all GROQ keys from .env — GROQ_API_KEY, GROQ_API_KEY_2, GROQ_API_KEY_3 ..."""
    keys = []
    # Main key
    if os.getenv("GROQ_API_KEY"):
        keys.append(os.getenv("GROQ_API_KEY"))
    # Extra keys
    i = 2
    while True:
        key = os.getenv(f"GROQ_API_KEY_{i}")
        if not key:
            break
        keys.append(key)
        i += 1
    return keys

GROQ_KEYS = _load_groq_keys()
_groq_key_index = 0  # Current active key

def _get_groq_key() -> str:
    return GROQ_KEYS[_groq_key_index] if GROQ_KEYS else ""

def _rotate_groq_key():
    global _groq_key_index
    _groq_key_index = (_groq_key_index + 1) % len(GROQ_KEYS)
    print(f"Rotated to Groq key #{_groq_key_index + 1}")
    Speak("Switching to backup API.")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL   = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Conversation history
conversation_history = []

# ══════════════════════════════════════════════════════
# APP MAP
# ══════════════════════════════════════════════════════

USERNAME = os.getenv("USERNAME", "User")
APP_MAP = {
    "whatsapp":     rf"C:\Users\{USERNAME}\AppData\Local\WhatsApp\WhatsApp.exe",
    "chrome":       r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":      r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad":      "notepad.exe",
    "calculator":   "calc.exe",
    "explorer":     "explorer.exe",
    "file manager": "explorer.exe",
    "vs code":      rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode":       rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify":      rf"C:\Users\{USERNAME}\AppData\Roaming\Spotify\Spotify.exe",
    "telegram":     rf"C:\Users\{USERNAME}\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "discord":      rf"C:\Users\{USERNAME}\AppData\Local\Discord\Update.exe",
    "paint":        "mspaint.exe",
    "vlc":          r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "task manager": "taskmgr.exe",
    "figma":        rf"C:\Users\{USERNAME}\AppData\Local\Figma\Figma.exe",
    "word":         r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":        r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
}

# ══════════════════════════════════════════════════════
# GROQ — Main Brain with auto key rotation
# ══════════════════════════════════════════════════════

SYSTEM_PROMPT = """You are Jarvis, an advanced AI personal assistant running on Windows.
You can control the computer, answer questions, and help with tasks.

Respond ONLY with a JSON object:
{
  "type": "action|conversation|vision",
  "intent": "open_app|close_app|web_search|system_control|type_text|email|conversation|vision_task",
  "target": "specific target",
  "response": "what to say to user",
  "data": {}
}

ROUTING RULES — follow strictly:
- open app/software → type=action, intent=open_app, target=app name
- web search/open website → type=action, intent=web_search, target=query, data={url:...}
- lock/shutdown/volume/mute/screenshot → type=action, intent=system_control, target=action
- email/compose mail → type=action, intent=email, target=recipient
- close app → type=action, intent=close_app, target=app name
- ANY clicking on screen/buttons/UI elements → type=vision
- reading/seeing screen → type=vision  
- send whatsapp/interact with open app → type=vision
- drag drop/scroll in app → type=vision
- general chat/questions/jokes → type=conversation

Examples:
"open chrome" → {"type":"action","intent":"open_app","target":"chrome","response":"Opening Chrome.","data":{}}
"search youtube" → {"type":"action","intent":"web_search","target":"youtube","response":"Opening YouTube.","data":{"url":"https://youtube.com"}}
"lock pc" → {"type":"action","intent":"system_control","target":"lock","response":"Locking PC.","data":{}}
"close notepad" → {"type":"action","intent":"close_app","target":"notepad","response":"Closing Notepad.","data":{}}
"what do you see" → {"type":"vision","intent":"vision_task","target":"describe screen","response":"Let me look at your screen.","data":{}}
"click send button" → {"type":"vision","intent":"vision_task","target":"click send button","response":"Finding send button.","data":{}}
"send hi to arpit on whatsapp" → {"type":"vision","intent":"vision_task","target":"find arpit on whatsapp and send hi","response":"Working on it.","data":{}}
"tell me a joke" → {"type":"conversation","intent":"conversation","target":"","response":"Why don't scientists trust atoms? Because they make up everything!","data":{}}

Always respond ONLY with valid JSON. No markdown, no explanation."""


def groq_call(user_message: str, add_to_history: bool = True) -> dict:
    """Groq call with auto key rotation on limit."""
    global conversation_history, _groq_key_index

    if not GROQ_KEYS:
        return {"type": "conversation", "intent": "conversation",
                "response": "No Groq API key configured.", "data": {}}

    if add_to_history:
        conversation_history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history[-8:]  # Last 8 only — token save

    # Try all keys
    for attempt in range(len(GROQ_KEYS)):
        try:
            response = requests.post(
                GROQ_URL,
                headers={
                    "Authorization": f"Bearer {_get_groq_key()}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": GROQ_MODEL,
                    "messages": messages,
                    "temperature": 0.2,
                    "max_tokens": 250,
                    "response_format": {"type": "json_object"}
                },
                timeout=15
            )

            # Rate limit hit → rotate key
            if response.status_code == 429:
                print(f"Key #{_groq_key_index + 1} exhausted.")
                _rotate_groq_key()
                continue

            result = response.json()
            text = result["choices"][0]["message"]["content"]
            data = json.loads(text)

            if add_to_history:
                conversation_history.append({"role": "assistant", "content": text})

            return data

        except Exception as e:
            print(f"Groq error (key #{_groq_key_index + 1}): {e}")
            _rotate_groq_key()
            continue

    return {"type": "conversation", "intent": "conversation",
            "response": "All API keys exhausted. Please add more.", "data": {}}


# ══════════════════════════════════════════════════════
# GEMINI VISION — Fixed
# ══════════════════════════════════════════════════════

def gemini_see_screen(task: str) -> dict:
    """Screenshot → Gemini Flash → exact pixel coordinates."""

    screenshot = pyautogui.screenshot()
    screen_w, screen_h = pyautogui.size()

    # Resize to 1280 wide max — good balance of speed and accuracy
    if screen_w > 1280:
        ratio = 1280 / screen_w
        new_w = 1280
        new_h = int(screen_h * ratio)
        screenshot = screenshot.resize((new_w, new_h))
        scale_x = screen_w / new_w
        scale_y = screen_h / new_h
    else:
        scale_x = 1.0
        scale_y = 1.0
        new_w, new_h = screen_w, screen_h

    buffer = BytesIO()
    screenshot.save(buffer, format="JPEG", quality=85)
    screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()

    prompt = f"""You are controlling a Windows PC screen.
Image size: {new_w}x{new_h} pixels (scaled from {screen_w}x{screen_h}).

Task: {task}

Carefully look at the screenshot and find the element.
Return JSON ONLY:
{{
  "found": true,
  "description": "briefly what you see and plan to do",
  "action": "click|type|key|scroll|none",
  "x": 640,
  "y": 360,
  "text": "",
  "key": "",
  "complete": false
}}

IMPORTANT:
- x, y are coordinates in the SCALED image ({new_w}x{new_h})
- action=none only if task is already complete
- complete=true if the overall task is done
- Be very precise with x,y — look carefully at exact position"""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": screenshot_b64}}
            ]
        }],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 200}
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=20)
        resp_json = response.json()

        if "error" in resp_json:
            print(f"Gemini API error: {resp_json['error']}")
            return {"found": False, "description": "Gemini error", "complete": False}

        text = resp_json["candidates"][0]["content"]["parts"][0]["text"]
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1:
            result = json.loads(text[start:end])
            # Scale coordinates back to actual screen size
            if "x" in result:
                result["x"] = int(result["x"] * scale_x)
                result["y"] = int(result["y"] * scale_y)
            print(f"Vision: {result.get('description', '')} → ({result.get('x')}, {result.get('y')})")
            return result

    except Exception as e:
        print(f"Gemini vision error: {e}")

    return {"found": False, "description": "Could not read screen", "complete": False}


def execute_vision_action(vision_data: dict) -> bool:
    """Vision action execute karo with smooth mouse movement."""
    if not vision_data.get("found", False):
        return False

    action = vision_data.get("action", "none")
    if action == "none":
        return True

    x = vision_data.get("x", 0)
    y = vision_data.get("y", 0)

    try:
        if action == "click":
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.1)
            pyautogui.click(x, y)
            print(f"Clicked: ({x}, {y})")
            return True

        elif action == "type":
            text = vision_data.get("text", "")
            pyautogui.click(x, y)
            time.sleep(0.2)
            pyautogui.write(text, interval=0.04)
            return True

        elif action == "key":
            pyautogui.press(vision_data.get("key", "enter"))
            return True

        elif action == "scroll":
            pyautogui.scroll(-3, x=x, y=y)
            return True

    except Exception as e:
        print(f"Execute error: {e}")

    return False


def vision_agent_loop(task: str, max_steps: int = 6):
    """Agentic loop — screenshot → action → screenshot → action until done."""
    print(f"\nVision agent: {task}")

    for step_num in range(1, max_steps + 1):
        print(f"Vision step {step_num}/{max_steps}")

        result = gemini_see_screen(
            f"Task: {task}\n"
            f"This is step {step_num}. What action should I take now? "
            f"Set complete=true if task is fully done."
        )

        desc = result.get("description", "")
        print(f"  → {desc}")

        # Done?
        if result.get("complete", False) or not result.get("found", True):
            Speak("Done!")
            return True

        # Execute
        execute_vision_action(result)
        time.sleep(1.0)  # Screen settle hone do

    Speak("Task completed.")
    return True


# ══════════════════════════════════════════════════════
# DIRECT ACTIONS (no vision needed)
# ══════════════════════════════════════════════════════

def open_app(app_name: str) -> bool:
    app_lower = app_name.lower().strip()
    exe_path = APP_MAP.get(app_lower)

    if exe_path and os.path.exists(exe_path):
        subprocess.Popen(exe_path)
        return True

    # Windows search
    try:
        pyautogui.hotkey('win', 's')
        time.sleep(0.7)
        pyautogui.write(app_name, interval=0.05)
        time.sleep(1.0)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Open error: {e}")
        return False


def close_app(app_name: str) -> bool:
    app_lower = app_name.lower().strip()
    exe_path = APP_MAP.get(app_lower, app_lower)
    exe_name = os.path.basename(exe_path).replace(".exe", "") if "\\" in exe_path else exe_path

    result = subprocess.run(
        f"taskkill /f /im {exe_name}.exe",
        shell=True, capture_output=True
    )
    if result.returncode != 0:
        pyautogui.hotkey('alt', 'f4')
    return True


def web_search(target: str, url: str = "") -> bool:
    import webbrowser
    webbrowser.open(url if url else f"https://www.google.com/search?q={target}")
    return True


def system_control(target: str) -> bool:
    t = target.lower()
    actions = {
        "lock":        lambda: subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True),
        "shutdown":    lambda: subprocess.run("shutdown /s /t 3", shell=True),
        "restart":     lambda: subprocess.run("shutdown /r /t 3", shell=True),
        "volume up":   lambda: [pyautogui.press("volumeup") for _ in range(5)],
        "volume down": lambda: [pyautogui.press("volumedown") for _ in range(5)],
        "mute":        lambda: pyautogui.press("volumemute"),
        "screenshot":  lambda: pyautogui.screenshot(
            os.path.expanduser(f"~/Pictures/jarvis_{int(time.time())}.png")
        ),
    }
    for key, action in actions.items():
        if key in t:
            action()
            return True
    return False


def _handle_email(recipient: str, data: dict):
    from core.voice import TakeCommand
    Speak("What should the email be about?")
    about = TakeCommand()

    email_result = groq_call(
        f"Write a professional email to {recipient} about: {about}. "
        f"Return JSON: {{\"subject\": \"...\", \"body\": \"...\"}}",
        add_to_history=False
    )

    subject = email_result.get("subject", "Important Message")
    body = email_result.get("body", about)

    import webbrowser, urllib.parse
    gmail_url = (
        f"https://mail.google.com/mail/?view=cm"
        f"&to={urllib.parse.quote(recipient)}"
        f"&su={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )
    webbrowser.open(gmail_url)
    Speak(f"Email ready. Subject: {subject}. Please review and send.")


# ══════════════════════════════════════════════════════
# MAIN BRAIN
# ══════════════════════════════════════════════════════

def process_command(command: str) -> bool:
    result = groq_call(command)

    response_text = result.get("response", "")
    cmd_type      = result.get("type", "conversation")
    intent        = result.get("intent", "conversation")
    target        = result.get("target", "")
    data          = result.get("data", {})

    print(f"Type={cmd_type} | Intent={intent} | Target={target}")

    if response_text:
        Speak(response_text)

    if cmd_type == "action":
        if   intent == "open_app":       open_app(target)
        elif intent == "close_app":      close_app(target)
        elif intent == "web_search":     web_search(target, data.get("url", ""))
        elif intent == "system_control": system_control(target)
        elif intent == "email":          _handle_email(target, data)
        elif intent == "type_text":      pyautogui.write(data.get("text", target), interval=0.04)

    elif cmd_type == "vision":
        vision_agent_loop(target or command)

    elif cmd_type == "conversation":
        pass  # Already spoken above

    return True


def chat_with_llm(query: str) -> str:
    result = groq_call(query)
    return result.get("response", "")