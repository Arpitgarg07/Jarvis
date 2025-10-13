import json
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

TASKS_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "tasks.json",
)


def _ensure_storage() -> None:
    os.makedirs(os.path.dirname(TASKS_FILE), exist_ok=True)
    if not os.path.exists(TASKS_FILE):
        _save_tasks([])


def _load_tasks() -> List[Dict]:
    _ensure_storage()
    try:
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_tasks(tasks: List[Dict]) -> None:
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def _normalize_priority(priority: Optional[str]) -> str:
    if not priority:
        return "normal"
    priority = priority.strip().lower()
    if priority in ("high", "urgent", "priority high"):
        return "high"
    if priority in ("low", "priority low"):
        return "low"
    return "normal"


def _parse_deadline(text: str) -> Optional[str]:
    if not text:
        return None
    text = text.lower().strip()

    now = datetime.now()

    # today / tomorrow
    if "today" in text:
        base = now
    elif "tomorrow" in text:
        base = now + timedelta(days=1)
    else:
        base = None

    # weekday names
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    for name, idx in weekdays.items():
        if name in text:
            days_ahead = (idx - now.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            base = now + timedelta(days=days_ahead)
            break

    # time like 5 pm, 17:30, 8:00 am
    hour = 9
    minute = 0
    time_match = re.search(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", text)
    if time_match:
        hour = int(time_match.group(1))
        minute = int(time_match.group(2) or 0)
        meridiem = (time_match.group(3) or "").lower()
        if meridiem:
            if meridiem == "pm" and hour < 12:
                hour += 12
            if meridiem == "am" and hour == 12:
                hour = 0

    if base is None:
        # If only time is present, assume today (or tomorrow if time already passed)
        candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if candidate < now:
            candidate = candidate + timedelta(days=1)
        return candidate.isoformat()

    candidate = base.replace(hour=hour, minute=minute, second=0, microsecond=0)
    return candidate.isoformat()


def add_task(
    description: str,
    deadline_text: Optional[str] = None,
    priority: Optional[str] = None,
) -> Dict:
    tasks = _load_tasks()
    task = {
        "id": int(datetime.now().timestamp() * 1000),
        "title": description.strip(),
        "priority": _normalize_priority(priority),
        "deadline": _parse_deadline(deadline_text) if deadline_text else None,
        "completed": False,
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
    }
    tasks.append(task)
    _save_tasks(tasks)
    return task


def list_tasks(period: Optional[str] = None) -> List[Dict]:
    tasks = _load_tasks()
    if not period:
        return tasks
    now = datetime.now()
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        result = []
        for t in tasks:
            if not t.get("deadline"):
                continue
            dt = datetime.fromisoformat(t["deadline"])
            if start <= dt <= end and not t.get("completed"):
                result.append(t)
        return result
    if period == "week":
        start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end = start + timedelta(days=7)
        result = []
        for t in tasks:
            if not t.get("deadline"):
                continue
            dt = datetime.fromisoformat(t["deadline"])
            if start <= dt < end and not t.get("completed"):
                result.append(t)
        return result
    return tasks


def overdue_tasks() -> List[Dict]:
    tasks = _load_tasks()
    now = datetime.now()
    result = []
    for t in tasks:
        if t.get("completed"):
            continue
        dl = t.get("deadline")
        if not dl:
            continue
        try:
            dt = datetime.fromisoformat(dl)
            if dt < now:
                result.append(t)
        except Exception as e:
            print(f"Error parsing deadline for task {t.get('title', 'Unknown')}: {e}")
            # Skip this task if deadline parsing fails
    return result


def mark_completed(title_query: str) -> Optional[Dict]:
    tasks = _load_tasks()
    for t in tasks:
        if t["title"].lower() == title_query.lower() and not t.get("completed"):
            t["completed"] = True
            t["completed_at"] = datetime.now().isoformat()
            _save_tasks(tasks)
            return t
    return None


def set_priority(title_query: str, priority: str) -> Optional[Dict]:
    tasks = _load_tasks()
    for t in tasks:
        if t["title"].lower() == title_query.lower():
            t["priority"] = _normalize_priority(priority)
            _save_tasks(tasks)
            return t
    return None


def format_task(t: Dict) -> str:
    title = t.get("title")
    pr = t.get("priority", "normal")
    dl = t.get("deadline")
    status = "done" if t.get("completed") else "pending"
    when = datetime.fromisoformat(dl).strftime("%a %I:%M %p") if dl else "no deadline"
    return f"[{pr}] {title} — {when} ({status})"


def summary_text(period: str) -> str:
    if period == "today":
        items = list_tasks("today")
        if not items:
            return "You have no tasks for today."
        return "Today's tasks: " + "; ".join(format_task(t) for t in items[:10])
    if period == "week":
        items = list_tasks("week")
        if not items:
            return "You have no tasks this week."
        return "This week's tasks: " + "; ".join(format_task(t) for t in items[:10])
    if period == "overdue":
        items = overdue_tasks()
        if not items:
            return "You have no overdue tasks."
        return "Overdue tasks: " + "; ".join(format_task(t) for t in items[:10])
    return ""
