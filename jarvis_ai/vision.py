"""
jarvis_ai/vision.py
────────────────────
Hybrid Vision System

Philosophy:
- 90% tasks = keyboard shortcuts (INSTANT, zero hallucination)
- 10% tasks = single-shot vision (1 screenshot → 1 action, no loops)

No more 5-step loops. No more wrong coordinates.
"""

import os, base64, json, time, requests
from io import BytesIO
import pyautogui
from dotenv import load_dotenv
load_dotenv()

# ── Gemini Vision Setup ───────────────────────────────
GEMINI_KEY   = os.getenv("GEMINI_API_KEY", "")
VISION_MODEL = "gemini-2.5-flash"
GEMINI_URL   = f"https://generativelanguage.googleapis.com/v1beta/models/{VISION_MODEL}:generateContent"
THUMB_W, THUMB_H = 1280, 720


# ══════════════════════════════════════════════════════
# LAYER 1 — Keyboard Shortcuts (INSTANT, no AI)
# ══════════════════════════════════════════════════════

# task keyword → (shortcut, description)
SHORTCUTS = {
    # Browser
    "address bar":       (("ctrl", "l"),     "focus"),
    "search bar chrome": (("ctrl", "l"),     "focus"),
    "new tab":           (("ctrl", "t"),     "press"),
    "close tab":         (("ctrl", "w"),     "press"),
    "back":              (("alt", "left"),   "focus"),
    "forward":           (("alt", "right"),  "focus"),
    "refresh":           (("ctrl", "r"),     "press"),
    "zoom in":           (("ctrl", "="),     "press"),
    "zoom out":          (("ctrl", "-"),     "press"),
    "fullscreen":        ("f11",             "single"),
    "find on page":      (("ctrl", "f"),     "focus"),

    # Scroll
    "scroll down":       None,   # handled specially
    "scroll up":         None,
    "scroll":            None,

    # WhatsApp / apps
    "search box whatsapp": (("ctrl", "f"), "focus"),
    "new chat whatsapp":   (("ctrl", "n"), "focus"),

    # System
    "copy":              (("ctrl", "c"),  "press"),
    "paste":             (("ctrl", "v"),  "press"),
    "select all":        (("ctrl", "a"),  "press"),
    "undo":              (("ctrl", "z"),  "press"),
    "save":              (("ctrl", "s"),  "press"),
    "close window":      (("alt", "f4"), "press"),
    "minimize":          (("win", "down"), "press"),
    "maximize":          (("win", "up"),   "press"),
    "switch app":        (("alt", "tab"),  "press"),
    "task manager":      (("ctrl", "shift", "esc"), "press"),
    "screenshot":        (("win", "shift", "s"),    "press"),
}


def try_shortcut(task: str) -> bool:
    """
    Task ke liye keyboard shortcut try karo.
    Returns True if shortcut found and executed.
    """
    task_lower = task.lower()

    # Scroll specially handle karo
    if "scroll down" in task_lower or "scroll down" in task_lower:
        amount = -10
        if "fast" in task_lower or "lot" in task_lower: amount = -20
        pyautogui.scroll(amount)
        return True
    if "scroll up" in task_lower:
        amount = 10
        pyautogui.scroll(amount)
        return True
    if task_lower.strip() == "scroll":
        pyautogui.scroll(-10)
        return True

    # Shortcut map check
    for keyword, shortcut in SHORTCUTS.items():
        if keyword in task_lower and shortcut is not None:
            if isinstance(shortcut[0], tuple) or isinstance(shortcut[0], str):
                keys = shortcut[0] if isinstance(shortcut[0], tuple) else shortcut[0]
                if isinstance(keys, tuple):
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(keys)
            return True

    return False  # No shortcut found


# ══════════════════════════════════════════════════════
# LAYER 2 — Single Shot Vision (1 screenshot, 1 action)
# ══════════════════════════════════════════════════════

def _screenshot_b64():
    screen = pyautogui.screenshot()
    rw, rh = pyautogui.size()
    thumb  = screen.resize((THUMB_W, THUMB_H))
    buf    = BytesIO()
    thumb.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode(), rw, rh


def _vision_call(prompt: str, b64: str) -> dict:
    """Single Gemini vision call."""
    if not GEMINI_KEY:
        print("Vision: GEMINI_API_KEY not set")
        return {"found": False}
    try:
        r = requests.post(
            f"{GEMINI_URL}?key={GEMINI_KEY}",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
            ]}],
            "generationConfig": {"temperature": 0.0, "maxOutputTokens": 256,
                                 "responseMimeType": "application/json"}},
            timeout=20)

        if r.status_code == 429:
            print("Vision: Gemini rate limited, retrying in 2s...")
            time.sleep(2)
            r = requests.post(
                f"{GEMINI_URL}?key={GEMINI_KEY}",
                headers={"Content-Type": "application/json"},
                json={"contents": [{"parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": b64}}
                ]}],
                "generationConfig": {"temperature": 0.0, "maxOutputTokens": 256,
                                     "responseMimeType": "application/json"}},
                timeout=20)

        if r.status_code != 200:
            print(f"Vision {r.status_code}: {r.text[:100]}")
            return {"found": False}

        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        s, e = text.find("{"), text.rfind("}") + 1
        if s != -1:
            return json.loads(text[s:e])

    except Exception as ex:
        print(f"Vision err: {ex}")

    return {"found": False}


def single_shot_click(element: str) -> bool:
    """
    One screenshot → find element → click.
    No loops, no retries — instant.
    """
    b64, rw, rh = _screenshot_b64()

    prompt = f"""Windows PC screenshot ({THUMB_W}x{THUMB_H} pixels).

Find: "{element}"

Return the CENTER of that element as PERCENTAGE of image dimensions.
x_pct: 0=left edge, 100=right edge
y_pct: 0=top edge, 100=bottom edge

JSON ONLY:
{{"found": true, "x_pct": 45.2, "y_pct": 8.5, "description": "search bar at top"}}
or
{{"found": false, "x_pct": 0, "y_pct": 0, "description": "not visible"}}"""

    result = _vision_call(prompt, b64)
    desc = result.get("description", "")
    print(f"Vision: {desc} → {result.get('x_pct')}%, {result.get('y_pct')}%")

    if not result.get("found", False):
        return False

    # Percentage → actual pixels
    x = int(max(0, min(100, result.get("x_pct", 50))) * rw / 100)
    y = int(max(0, min(100, result.get("y_pct", 50))) * rh / 100)

    print(f"Click → ({x}, {y}) on {rw}x{rh} screen")
    pyautogui.moveTo(x, y, duration=0.3)
    time.sleep(0.1)
    pyautogui.click(x, y)
    return True


# ══════════════════════════════════════════════════════
# PUBLIC API
# ══════════════════════════════════════════════════════

def describe_screen() -> str:
    """Screen describe karo."""
    b64, rw, rh = _screenshot_b64()
    result = _vision_call(
        'Describe this Windows PC screenshot in 2-3 sentences. '
        'What apps are open? What is visible? '
        'Return JSON: {"description": "..."}', b64)
    return result.get("description", "I can see your screen.")


def find_and_click(element: str) -> bool:
    """Shortcut try karo, nahi toh vision use karo."""
    if try_shortcut(element):
        print(f"Shortcut used for: {element}")
        return True
    return single_shot_click(element)


def vision_agent_loop(task: str, max_steps: int = 4) -> bool:
    """
    Multi-step tasks ke liye.
    But PEHLE shortcut check karo — loop sirf last resort.
    """
    from core.voice import Speak

    # Simple tasks → shortcut se karo
    if try_shortcut(task):
        return True

    print(f"\nVision agent: {task}")

    for step in range(1, max_steps + 1):
        print(f"Step {step}/{max_steps}")
        b64, rw, rh = _screenshot_b64()

        prompt = f"""Windows PC screenshot ({THUMB_W}x{THUMB_H}).

TASK: {task}
STEP: {step}/{max_steps}

What is the SINGLE next action?

JSON ONLY:
{{
  "complete": false,
  "action": "click|type|key|scroll_down|scroll_up|wait",
  "x_pct": 50.0,
  "y_pct": 25.0,
  "text": "",
  "key": "",
  "description": "I see X, doing Y"
}}

RULES:
- x_pct/y_pct = 0-100 percentage (NOT pixels, NOT grid)
- scroll_down/scroll_up: no coordinates needed
- complete=true when task is FULLY done
- ONE action per step only"""

        result = _vision_call(prompt, b64)
        if not result:
            break

        desc = result.get("description", "")
        print(f"  {desc}")

        if result.get("complete", False):
            Speak("Done!")
            return True

        action = result.get("action", "none")

        if action == "click":
            xp = max(0, min(100, result.get("x_pct", 50)))
            yp = max(0, min(100, result.get("y_pct", 50)))
            x  = int(xp * rw / 100)
            y  = int(yp * rh / 100)
            print(f"  → Click ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.3)
            time.sleep(0.1)
            pyautogui.click(x, y)

        elif action == "type":
            txt = result.get("text", "")
            print(f"  → Type: {txt}")
            pyautogui.write(txt, interval=0.05)

        elif action == "key":
            k = result.get("key", "enter")
            print(f"  → Key: {k}")
            pyautogui.press(k)

        elif action == "scroll_down":
            pyautogui.scroll(-8)

        elif action == "scroll_up":
            pyautogui.scroll(8)

        elif action == "wait":
            time.sleep(2)

        time.sleep(0.6)

    Speak("Done.")
    return True