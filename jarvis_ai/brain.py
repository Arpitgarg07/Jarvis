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


# ── System Prompt — English Only ───────────────────────
SYSTEM_PROMPT = """You are Jarvis, a personal AI assistant created by Arpit Garg.

PERSONALITY: Talk like a real person — natural, warm, casual. Not robotic. Use short sentences where possible. React to what the user says, not just answer. If they say "ok ok" or "wait", you already stopped — that's handled separately. Keep responses concise unless the user asks for detail.

IDENTITY: ONLY if the user directly asks "who made you", "who created you", "who built you", "who is your programmer" — say "I was created by Arpit Garg." Never mention this otherwise.

LANGUAGE: Always respond in English only.

MEMORY: You have access to conversation history. Refer back to it naturally when relevant. If the user says "you were saying" or "continue", the app handles replaying — don't repeat yourself unless asked.

Respond ONLY with JSON:
{
  "type": "action|vision|conversation",
  "intent": "open_app|close_app|web_search|system_control|email|conversation|vision_task",
  "target": "specific target",
  "response": "what to say — natural, human tone",
  "data": {}
}

ROUTING — strictly follow:
- Open an app → type=action, intent=open_app
- Website/search → type=action, intent=web_search, data={url:...}
- Lock/shutdown/volume → type=action, intent=system_control
- Close an app → type=action, intent=close_app
- Click/type/interact on screen → type=vision
- Describe screen → type=vision
- Send WhatsApp message → type=vision
- Scroll/navigate page → type=vision
- General conversation/question → type=conversation

Examples:
"open chrome" → {"type":"action","intent":"open_app","target":"chrome","response":"Sure, opening Chrome.","data":{}}
"search wikipedia" → {"type":"action","intent":"web_search","target":"wikipedia","response":"On it.","data":{"url":"https://wikipedia.org"}}
"send whatsapp message to Arpit" → {"type":"vision","intent":"vision_task","target":"open arpit chat on whatsapp and type message","response":"Looking for Arpit's chat.","data":{}}
"what do you see on screen" → {"type":"vision","intent":"vision_task","target":"describe screen","response":"Let me take a look.","data":{}}
"tell me a joke" → {"type":"conversation","intent":"conversation","target":"","response":"Why don't scientists trust atoms? Because they make up everything!","data":{}}
"how are you" → {"type":"conversation","intent":"conversation","target":"","response":"Doing great, thanks for asking! What can I do for you?","data":{}}

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


def _take_command_retry(prompt: str, retries: int = 3) -> str:
    """Speak prompt, wait for mic to settle, then listen. Retries on failure."""
    for attempt in range(retries):
        Speak(prompt if attempt == 0 else "Sorry, I didn't catch that. Please say it again.")
        time.sleep(0.7)
        result = TakeCommand()
        if result != "None":
            return result
    return "None"


def handle_email(recipient: str, data: dict, original_command: str = ""):
    import re, requests as _req, smtplib
    from email.message import EmailMessage
    from features.communication.sendemail import RECIPIENT_MAPPING, send_email
    from dotenv import load_dotenv
    load_dotenv()

    def _cancel():
        Speak("Okay, email cancelled.")

    # ── Step 1: get recipient name ────────────────────────
    # First try to extract from what user originally said
    if not recipient or recipient.lower() in ("", "email client", "none"):
        match = re.search(
            r"(?:to|for)\s+([A-Za-z ]{2,40}?)(?:\s+about|\s+regarding|$)",
            original_command, re.IGNORECASE)
        if match:
            recipient = match.group(1).strip()

    if not recipient or recipient.lower() in ("", "email client", "none"):
        recipient = _take_command_retry("Who do you want to send the email to?")
        if recipient == "None":
            return _cancel()

    # ── Step 2: resolve email address ────────────────────
    email_addr = RECIPIENT_MAPPING.get(recipient.lower().strip(), "")
    if not email_addr and "@" in recipient:
        email_addr = recipient.strip()
    if not email_addr:
        email_addr = _take_command_retry(
            f"I don't have {recipient}'s email address. Please say their email address.")
        if email_addr == "None":
            return _cancel()
        # Clean up speech-to-text email artifacts:
        # "arpitgarg5689 at the rate gmail.com" → "arpitgarg5689@gmail.com"
        email_addr = (email_addr.lower()
                      .replace(" at the rate ", "@")
                      .replace(" at ", "@")
                      .replace(" dot ", ".")
                      .replace(" ", ""))

    # ── Step 3: get subject ───────────────────────────────
    subject = _take_command_retry("What is the subject of the email?")
    if subject == "None":
        return _cancel()

    # ── Step 4: get body ──────────────────────────────────
    body_input = _take_command_retry("Now tell me what to write in the email body.")
    if body_input == "None":
        return _cancel()

    # ── Step 5: AI-polish the body ────────────────────────
    Speak("Drafting your email, one moment.")
    body = body_input
    try:
        r = _req.post(GROQ_URL,
            headers={"Authorization": f"Bearer {_get_key()}",
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content":
                      f"Write a professional email body to {recipient}. "
                      f"Subject: {subject}. Content: {body_input}. "
                      f"Return ONLY JSON: {{\"body\": \"...\"}}"}],
                  "temperature": 0.4, "max_tokens": 400,
                  "response_format": {"type": "json_object"}},
            timeout=15)
        import json as _json
        body = _json.loads(r.json()["choices"][0]["message"]["content"]).get("body", body_input)
    except Exception as e:
        print(f"Email draft error: {e}")
        body = body_input

    # ── Step 6: show full summary for confirmation ────────
    print("\n" + "="*50)
    print("EMAIL SUMMARY")
    print("="*50)
    print(f"  To      : {recipient} <{email_addr}>")
    print(f"  Subject : {subject}")
    print(f"  Body    :\n{body}")
    print("="*50 + "\n")

    confirm = _take_command_retry(
        f"Here is your email. To: {recipient}. Subject: {subject}. "
        f"Body starts with: {body[:80]}. "
        f"Should I send it? Say yes to send or no to cancel.")

    if confirm == "None" or not any(w in confirm.lower() for w in ["yes","send","ok","yeah","sure","go ahead","confirm"]):
        return _cancel()

    # ── Step 7: send via SMTP ─────────────────────────────
    Speak("Sending your email now.")
    try:
        send_email(email_addr, subject, body)
        Speak(f"Done! Email sent to {recipient} successfully.")
    except Exception as e:
        print(f"Send error: {e}")
        Speak("Sorry, I could not send the email. Please check your credentials.")


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
        elif intent == "email":          handle_email(target, data, command)
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