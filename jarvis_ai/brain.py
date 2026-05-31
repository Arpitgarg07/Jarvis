"""
jarvis_ai/brain.py
───────────────────
Jarvis AI Brain — Groq + Gemini Vision + UIAutomation

Stack:
- Groq Llama 3.3 70B  → Intent + Conversation (fast, smart, free)
- Gemini Flash        → Screen vision (free, accurate)
- UIAutomation        → Instant Windows actions
- PyAutoGUI           → Mouse/keyboard execution
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

GROQ_API_KEY  = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_MODEL    = "llama-3.3-70b-versatile"
GROQ_URL      = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL    = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Conversation history — Jarvis ko context yaad rehga
conversation_history = []

# ══════════════════════════════════════════════════════
# APP MAP
# ══════════════════════════════════════════════════════

USERNAME = os.getenv("USERNAME", "User")
APP_MAP = {
    "whatsapp":      rf"C:\Users\{USERNAME}\AppData\Local\WhatsApp\WhatsApp.exe",
    "chrome":        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":       r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad":       "notepad.exe",
    "calculator":    "calc.exe",
    "explorer":      "explorer.exe",
    "file manager":  "explorer.exe",
    "vs code":       rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode":        rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify":       rf"C:\Users\{USERNAME}\AppData\Roaming\Spotify\Spotify.exe",
    "telegram":      rf"C:\Users\{USERNAME}\AppData\Roaming\Telegram Desktop\Telegram.exe",
    "discord":       rf"C:\Users\{USERNAME}\AppData\Local\Discord\Update.exe",
    "paint":         "mspaint.exe",
    "vlc":           r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "task manager":  "taskmgr.exe",
    "word":          r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":         r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "figma":         rf"C:\Users\{USERNAME}\AppData\Local\Figma\Figma.exe",
}


# ══════════════════════════════════════════════════════
# GROQ — Main Brain
# ══════════════════════════════════════════════════════
SYSTEM_PROMPT = """You are Jarvis, an advanced AI personal assistant running on Windows.
You can control the computer, answer questions, and help with tasks.

When user gives a command, respond with a JSON object ONLY:
{
  "type": "action|conversation|vision",
  "intent": "open_app|close_app|web_search|system_control|type_text|click|conversation|vision_task|email|multi_step",
  "target": "specific target",
  "steps": ["step1", "step2"],
  "response": "what to say to user",
  "data": {}
}

Types:
- action: computer control task
- conversation: talking, questions, jokes, general chat
- vision: user wants you to see screen

Intent examples:
- "open chrome" → {"type":"action","intent":"open_app","target":"chrome","response":"Opening Chrome for you.","steps":[],"data":{}}
- "search wikipedia on chrome" → {"type":"action","intent":"web_search","target":"wikipedia","response":"Searching Wikipedia.","steps":["open chrome","search wikipedia"],"data":{"url":"https://wikipedia.org"}}
- "what is AI" → {"type":"conversation","intent":"conversation","target":"","response":"AI stands for Artificial Intelligence...","steps":[],"data":{}}
- "compose email to Rohit about meeting" → {"type":"action","intent":"email","target":"rohit","response":"I will compose a professional email. What should the email say?","steps":["open gmail","compose","fill details"],"data":{}}
- "what do you see on screen" → {"type":"vision","intent":"vision_task","target":"describe screen","response":"Let me look at your screen.","steps":[],"data":{}}
- "lock the pc" → {"type":"action","intent":"system_control","target":"lock","response":"Locking your PC.","steps":[],"data":{}}

CRITICAL ROUTING RULES:
- For ANY UI task needing clicks (close app by clicking X, send whatsapp message, click a button): use type="vision" so vision_agent_loop handles it step by step
- For "close X app" via clicking: use type="vision", target="close X window by clicking the X button"
- For multi-step UI tasks (open whatsapp → search person → send message): use type="vision"
- For simple app open: use type="action", intent="open_app" 
- For web search: use type="action", intent="web_search"
- For system commands (lock, shutdown, volume): use type="action", intent="system_control"
- NEVER use vision for simple open_app or web_search

Always respond ONLY with valid JSON. No extra text."""

def groq_call(user_message: str, add_to_history: bool = True) -> dict:
    """Groq Llama 3.3 70B se response lo."""
    global conversation_history

    if add_to_history:
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

    # Last 10 messages hi bhejo — token save
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history[-10:]

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 300,
                "response_format": {"type": "json_object"}
            },
            timeout=15
        )

        result = response.json()
        text = result["choices"][0]["message"]["content"]
        data = json.loads(text)

        # History mein add karo
        if add_to_history:
            conversation_history.append({
                "role": "assistant",
                "content": text
            })

        return data

    except Exception as e:
        print(f"Groq error: {e}")
        return {
            "type": "conversation",
            "intent": "conversation",
            "response": "Sorry, I had trouble processing that.",
            "steps": [],
            "data": {}
        }


# ══════════════════════════════════════════════════════
# GEMINI VISION — Screen dekhna
# ══════════════════════════════════════════════════════

def take_screenshot_b64() -> str:
    screenshot = pyautogui.screenshot()
    screenshot = screenshot.resize(
        (screenshot.width // 2, screenshot.height // 2)
    )
    buffer = BytesIO()
    screenshot.save(buffer, format="JPEG", quality=75)
    return base64.b64encode(buffer.getvalue()).decode()


def gemini_see_screen(task: str) -> dict:
    """Full resolution screenshot → Gemini → exact pixel coordinates."""
    
    # Full resolution screenshot — resize mat karo
    screenshot = pyautogui.screenshot()
    screen_w, screen_h = screenshot.size
    
    buffer = BytesIO()
    screenshot.save(buffer, format="PNG")  # PNG for better accuracy
    screenshot_b64 = base64.b64encode(buffer.getvalue()).decode()

    prompt = f"""You are controlling a Windows PC. Screen resolution: {screen_w}x{screen_h} pixels.

Task: {task}

Look carefully at the screenshot. Find the exact element needed.

Respond with JSON ONLY:
{{
  "found": true,
  "description": "what you see and what you will do",
  "action": "click|type|key|move",
  "x": 450,
  "y": 230,
  "text": "",
  "key": ""
}}

x and y are EXACT PIXEL coordinates on the {screen_w}x{screen_h} screen.
Be very precise. Look at window title bars, buttons, icons carefully."""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {
                    "mime_type": "image/png",
                    "data": screenshot_b64
                }}
            ]
        }],
        "generationConfig": {
            "temperature": 0.0,
            "maxOutputTokens": 150
        }
    }

    try:
        response = requests.post(GEMINI_URL, json=payload, timeout=20)
        text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1:
            result = json.loads(text[start:end])
            print(f"Vision: {result.get('description', '')} → ({result.get('x')}, {result.get('y')})")
            return result
    except Exception as e:
        print(f"Gemini error: {e}")

    return {"found": False, "description": "Could not see screen"}


def execute_vision_action(vision_data: dict) -> bool:
    """Vision coordinates execute karo."""
    if not vision_data.get("found", False):
        Speak("I couldn't find that on screen.")
        return False

    action = vision_data.get("action", "click")
    x = vision_data.get("x", 0)
    y = vision_data.get("y", 0)

    if action == "click":
        # Cursor smoothly move karo phir click
        pyautogui.moveTo(x, y, duration=0.4)
        time.sleep(0.1)
        pyautogui.click(x, y)
        return True

    elif action == "type":
        text = vision_data.get("text", "")
        pyautogui.write(text, interval=0.04)
        return True

    elif action == "key":
        pyautogui.press(vision_data.get("key", ""))
        return True

    elif action == "move":
        pyautogui.moveTo(x, y, duration=0.4)
        return True

    return False


# ══════════════════════════════════════════════════════
# APP ACTIONS
# ══════════════════════════════════════════════════════

def open_app(app_name: str) -> bool:
    app_lower = app_name.lower().strip()
    exe_path = APP_MAP.get(app_lower)

    # Direct path se try karo
    if exe_path and os.path.exists(exe_path):
        subprocess.Popen(exe_path)
        return True

    # .exe naam se try karo
    try:
        subprocess.Popen(app_lower + ".exe")
        return True
    except Exception:
        pass

    # Windows search fallback
    try:
        pyautogui.hotkey('win', 's')
        time.sleep(0.7)
        pyautogui.write(app_name, interval=0.04)
        time.sleep(1.0)
        pyautogui.press('enter')
        return True
    except Exception as e:
        print(f"Open error: {e}")
        return False


def close_app(app_name: str) -> bool:
    app_lower = app_name.lower().strip()
    exe = APP_MAP.get(app_lower, app_lower)
    exe_name = os.path.basename(exe).replace(".exe", "") if "\\" in exe else exe

    result = subprocess.run(
        f"taskkill /f /im {exe_name}.exe",
        shell=True, capture_output=True
    )
    if result.returncode != 0:
        pyautogui.hotkey('alt', 'f4')
    return True


def web_search(target: str, url: str = "") -> bool:
    if url:
        webbrowser_url = url
    else:
        webbrowser_url = f"https://www.google.com/search?q={target}"

    try:
        import webbrowser
        webbrowser.open(webbrowser_url)
        return True
    except Exception:
        return False


def system_control(target: str) -> bool:
    t = target.lower()
    if "lock" in t:
        subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        return True
    elif "shutdown" in t:
        subprocess.run("shutdown /s /t 3", shell=True)
        return True
    elif "restart" in t:
        subprocess.run("shutdown /r /t 3", shell=True)
        return True
    elif "volume up" in t:
        for _ in range(5): pyautogui.press("volumeup")
        return True
    elif "volume down" in t:
        for _ in range(5): pyautogui.press("volumedown")
        return True
    elif "mute" in t:
        pyautogui.press("volumemute")
        return True
    elif "screenshot" in t:
        path = os.path.expanduser("~/Pictures/jarvis_screenshot.png")
        pyautogui.screenshot(path)
        Speak(f"Screenshot saved.")
        return True
    return False


# ══════════════════════════════════════════════════════
# MULTI-STEP EXECUTOR
# ══════════════════════════════════════════════════════

def execute_step(step: str, data: dict) -> bool:
    """Ek step execute karo."""
    step_lower = step.lower()

    if "open" in step_lower:
        app = step_lower.replace("open", "").strip()
        open_app(app)
        time.sleep(2)
        return True

    elif "search" in step_lower:
        query = step_lower.replace("search", "").strip()
        url = data.get("url", f"https://www.google.com/search?q={query}")
        web_search(query, url)
        time.sleep(2)
        return True

    elif "click" in step_lower:
        element = step_lower.replace("click", "").strip()
        time.sleep(1)
        vision_result = gemini_see_screen(f"click the {element}")
        return execute_vision_action(vision_result)

    elif "type" in step_lower or "write" in step_lower:
        text = data.get("text", "")
        if text:
            pyautogui.write(text, interval=0.03)
        return True

    elif "fill" in step_lower:
        time.sleep(1.5)
        vision_result = gemini_see_screen(step)
        return execute_vision_action(vision_result)

    return True


def vision_agent_loop(task: str, max_steps: int = 5):
    """
    Agentic loop — ek ek step vision se karo.
    Har step ke baad fresh screenshot lega.
    """
    Speak(f"Working on it.")
    
    for step in range(max_steps):
        # Fresh screenshot
        result = gemini_see_screen(
            f"Overall task: {task}. "
            f"Step {step+1}: What should I do next? "
            f"If task is complete, set found=false and description='Task complete'."
        )
        
        desc = result.get("description", "")
        print(f"Step {step+1}: {desc}")
        
        # Task complete check
        if "complete" in desc.lower() or "done" in desc.lower() or not result.get("found", True):
            Speak("Done!")
            return True
        
        # Action execute karo
        execute_vision_action(result)
        time.sleep(0.8)  # Next screenshot se pehle settle hone do
    
    return True

# ══════════════════════════════════════════════════════
# MAIN BRAIN
# ══════════════════════════════════════════════════════

def process_command(command: str) -> bool:
    """
    Main entry point.
    Returns True if handled, False = fallback to old COMMAND_MAP.
    """
    # Groq se intent lo
    result = groq_call(command)

    response_text = result.get("response", "")
    cmd_type = result.get("type", "conversation")
    intent = result.get("intent", "conversation")
    target = result.get("target", "")
    steps = result.get("steps", [])
    data = result.get("data", {})

    print(f"Type={cmd_type} | Intent={intent} | Target={target}")

    # Pehle response bolo
    if response_text:
        Speak(response_text)

    # Action execute karo
    if cmd_type == "action":
        if intent == "open_app":
            open_app(target)
        elif intent == "close_app":
            close_app(target)
        elif intent == "web_search":
            url = data.get("url", "")
            web_search(target, url)
        elif intent == "system_control":
            system_control(target)
        elif intent == "type_text":
            text = data.get("text", target)
            pyautogui.write(text, interval=0.03)
        elif intent == "email":
            _handle_email(target, data)
        elif intent == "click":
            vision_agent_loop(f"click {target}")

    elif cmd_type == "vision":
        vision_agent_loop(target or command)

    elif cmd_type == "conversation":
        pass
    return True


def _handle_email(recipient: str, data: dict):
    """Email compose karo — Groq professional email likhega."""
    from core.voice import TakeCommand

    Speak("What should the email be about?")
    email_content = TakeCommand()

    # Groq se professional email likhwao
    email_result = groq_call(
        f"Write a professional email to {recipient} about: {email_content}. "
        f"Return JSON with fields: subject, body",
        add_to_history=False
    )

    subject = email_result.get("subject", "Important Message")
    body = email_result.get("body", email_content)

    Speak(f"Email ready. Subject: {subject}. Opening Gmail now.")

    # Gmail open karo
    import webbrowser
    import urllib.parse
    encoded_body = urllib.parse.quote(body)
    encoded_subject = urllib.parse.quote(subject)
    gmail_url = f"https://mail.google.com/mail/?view=cm&to=&su={encoded_subject}&body={encoded_body}"
    webbrowser.open(gmail_url)

    Speak("Your email is ready in Gmail. Please review and send it.")


def chat_with_llm(query: str) -> str:
    """Direct conversation."""
    result = groq_call(query)
    return result.get("response", "")