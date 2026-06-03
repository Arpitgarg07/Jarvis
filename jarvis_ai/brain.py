"""
jarvis_ai/brain.py
───────────────────
Jarvis AI Brain — Clean Version

Stack:
- Groq Llama 3.3 70B  → Intent + Hinglish conversation
- vision.py           → Screen reading + clicking
- UIAutomation        → Instant Windows actions
"""

import os, json, time, requests, subprocess
import pyautogui
from dotenv import load_dotenv
from core.voice import Speak, TakeCommand
from jarvis_ai.vision import find_and_click, describe_screen, vision_agent_loop

load_dotenv()

# ── Groq Setup ─────────────────────────────────────────
def _load_keys():
    keys = []
    if os.getenv("GROQ_API_KEY"): keys.append(os.getenv("GROQ_API_KEY"))
    i = 2
    while True:
        k = os.getenv(f"GROQ_API_KEY_{i}")
        if not k: break
        keys.append(k); i += 1
    return keys

GROQ_KEYS = _load_keys()
_gidx = 0
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"
conversation_history = []

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
    "figma":        rf"C:\Users\{USERNAME}\AppData\Local\Figma\Figma.exe",
    "task manager": "taskmgr.exe",
}

def _get_key():
    return GROQ_KEYS[_gidx] if GROQ_KEYS else ""

def _rotate():
    global _gidx
    _gidx = (_gidx + 1) % len(GROQ_KEYS)


# ── System Prompt — Hinglish Support ───────────────────
SYSTEM_PROMPT = """You are Jarvis, an advanced AI personal assistant.

LANGUAGE: Respond in the SAME language the user speaks.
- If user speaks Hindi/Hinglish → respond in Hinglish
- If user speaks English → respond in English
- Mix naturally: "Opening Chrome kar raha hoon" or "Sure, search kar deta hoon"

Respond ONLY with JSON:
{
  "type": "action|vision|conversation",
  "intent": "open_app|close_app|web_search|system_control|email|conversation|vision_task",
  "target": "specific target",
  "response": "what to say (in user's language)",
  "data": {}
}

ROUTING — strictly follow:
- App open karna → type=action, intent=open_app
- Website/search → type=action, intent=web_search, data={url:...}
- Lock/shutdown/volume → type=action, intent=system_control
- App close → type=action, intent=close_app
- Screen pe click/type/interact → type=vision
- Kuch dekhna screen pe → type=vision
- WhatsApp pe message → type=vision
- Scroll/navigate page → type=vision
- Baat karna/sawaal → type=conversation

Examples:
"chrome khol" → {"type":"action","intent":"open_app","target":"chrome","response":"Chrome khol raha hoon.","data":{}}
"wikipedia search karo" → {"type":"action","intent":"web_search","target":"wikipedia","response":"Wikipedia khol raha hoon.","data":{"url":"https://wikipedia.org"}}
"WhatsApp pe Arpit ko message karo" → {"type":"vision","intent":"vision_task","target":"open arpit chat on whatsapp and type message","response":"WhatsApp pe Arpit ki chat dhundh raha hoon.","data":{}}
"screen pe kya dikh raha hai" → {"type":"vision","intent":"vision_task","target":"describe screen","response":"Screen dekh raha hoon.","data":{}}
"search box pe click karo" → {"type":"vision","intent":"vision_task","target":"click on search box","response":"Search box pe click kar raha hoon.","data":{}}
"scroll karo" → {"type":"vision","intent":"vision_task","target":"scroll down","response":"Scroll kar raha hoon.","data":{}}
"ek joke sunao" → {"type":"conversation","intent":"conversation","target":"","response":"Kya hua? Ek banda doctor ke paas gaya...","data":{}}

IMPORTANT: type=vision for ANY screen interaction. NEVER use action for clicking.
Always respond ONLY valid JSON. No markdown."""


def groq_call(message: str, add_history: bool = True) -> dict:
    global conversation_history, _gidx

    if add_history:
        conversation_history.append({"role": "user", "content": message})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += conversation_history[-8:]

    for _ in range(len(GROQ_KEYS)):
        try:
            r = requests.post(GROQ_URL,
                headers={"Authorization": f"Bearer {_get_key()}",
                         "Content-Type": "application/json"},
                json={"model": GROQ_MODEL, "messages": messages,
                      "temperature": 0.2, "max_tokens": 200,
                      "response_format": {"type": "json_object"}},
                timeout=15)

            if r.status_code == 429:
                _rotate(); continue

            if r.status_code != 200:
                print(f"Groq {r.status_code}: {r.text[:100]}")
                _rotate(); continue

            text = r.json()["choices"][0]["message"]["content"]
            data = json.loads(text)

            if add_history:
                conversation_history.append({"role": "assistant", "content": text})

            return data

        except Exception as e:
            print(f"Groq error: {e}"); _rotate()

    return {"type": "conversation", "intent": "conversation",
            "response": "Kuch problem aa gayi, dobara try karo.", "data": {}}


# ── Direct Actions ──────────────────────────────────────
def open_app(name: str) -> bool:
    path = APP_MAP.get(name.lower().strip())
    if path and os.path.exists(path):
        subprocess.Popen(path); return True
    try:
        pyautogui.hotkey('win', 's')
        time.sleep(0.7)
        pyautogui.write(name, interval=0.05)
        time.sleep(1.0)
        pyautogui.press('enter')
        return True
    except: return False


def close_app(name: str) -> bool:
    path = APP_MAP.get(name.lower().strip(), name)
    exe  = os.path.basename(path).replace(".exe","") if "\\" in path else path
    r    = subprocess.run(f"taskkill /f /im {exe}.exe",
                          shell=True, capture_output=True)
    if r.returncode != 0: pyautogui.hotkey('alt','f4')
    return True


def web_search(target: str, url: str = "") -> bool:
    import webbrowser
    webbrowser.open(url if url else f"https://www.google.com/search?q={target}")
    return True


def system_control(target: str) -> bool:
    t = target.lower()
    if "lock" in t:       subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
    elif "shutdown" in t: subprocess.run("shutdown /s /t 3", shell=True)
    elif "restart" in t:  subprocess.run("shutdown /r /t 3", shell=True)
    elif "volume up" in t:   [pyautogui.press("volumeup") for _ in range(5)]
    elif "volume down" in t: [pyautogui.press("volumedown") for _ in range(5)]
    elif "mute" in t:     pyautogui.press("volumemute")
    elif "screenshot" in t:
        p = os.path.expanduser(f"~/Pictures/jarvis_{int(time.time())}.png")
        pyautogui.screenshot(p); Speak("Screenshot le liya.")
    else: return False
    return True


def handle_email(recipient: str, data: dict):
    Speak("Email mein kya likhna hai?")
    about = TakeCommand()
    result = groq_call(
        f"Professional email likho {recipient} ko, topic: {about}. "
        f"JSON return karo: {{\"subject\": \"...\", \"body\": \"...\"}}",
        add_history=False)
    subject = result.get("subject", "Important Message")
    body    = result.get("body", about)
    import webbrowser, urllib.parse
    webbrowser.open(
        f"https://mail.google.com/mail/?view=cm"
        f"&to={urllib.parse.quote(recipient)}"
        f"&su={urllib.parse.quote(subject)}"
        f"&body={urllib.parse.quote(body)}"
    )
    Speak(f"Email ready hai. Subject: {subject}. Review karke send kar do.")


# ── Main Entry ──────────────────────────────────────────
def process_command(command: str) -> bool:
    result   = groq_call(command)
    cmd_type = result.get("type", "conversation")
    intent   = result.get("intent", "conversation")
    target   = result.get("target", "")
    response = result.get("response", "")
    data     = result.get("data", {})

    print(f"Type={cmd_type} | Intent={intent} | Target={target}")

    if response:
        Speak(response)

    if cmd_type == "action":
        if   intent == "open_app":       open_app(target)
        elif intent == "close_app":      close_app(target)
        elif intent == "web_search":     web_search(target, data.get("url",""))
        elif intent == "system_control": system_control(target)
        elif intent == "email":          handle_email(target, data)
        elif intent == "type_text":      pyautogui.write(data.get("text", target), interval=0.04)

    elif cmd_type == "vision":
        # Describe vs Act — clearly separate
        describe_keywords = ["kya dikh", "describe", "what do you see",
                             "screen pe kya", "dekho", "batao screen"]
        is_describe = any(k in (target + command).lower() for k in describe_keywords)

        if is_describe:
            desc = describe_screen()
            Speak(desc[:200] if len(desc) > 200 else desc)
        else:
            # ACTUALLY CLICK/INTERACT
            vision_agent_loop(target or command)

    # conversation — response already spoken
    return True


def chat_with_llm(query: str) -> str:
    return groq_call(query).get("response", "")