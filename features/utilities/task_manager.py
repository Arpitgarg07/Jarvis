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

    # Handle relative days
    if "next week" in text:
        base = now + timedelta(days=7)
    elif "next month" in text:
        # Simple approximation - add 30 days
        base = now + timedelta(days=30)
    elif "next year" in text:
        # Simple approximation - add 365 days
        base = now + timedelta(days=365)
    elif "today" in text:
        base = now
    elif "tomorrow" in text:
        base = now + timedelta(days=1)
    elif "day after tomorrow" in text:
        base = now + timedelta(days=2)
    elif "this week" in text:
        # Find next occurrence of the same weekday
        days_ahead = (6 - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        base = now + timedelta(days=days_ahead)
    elif "this weekend" in text:
        # Find next Saturday
        days_ahead = (5 - now.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        base = now + timedelta(days=days_ahead)
    else:
        base = None

    # weekday names
    weekdays = {
        "monday": 0, "mon": 0,
        "tuesday": 1, "tue": 1, "tues": 1,
        "wednesday": 2, "wed": 2,
        "thursday": 3, "thu": 3, "thur": 3, "thurs": 3,
        "friday": 4, "fri": 4,
        "saturday": 5, "sat": 5,
        "sunday": 6, "sun": 6,
    }
    
    for name, idx in weekdays.items():
        if name in text:
            days_ahead = (idx - now.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7
            base = now + timedelta(days=days_ahead)
            break

    # Handle specific dates (basic patterns)
    date_patterns = [
        r"(\d{1,2})/(\d{1,2})",  # MM/DD or DD/MM
        r"(\d{1,2})-(\d{1,2})",  # MM-DD or DD-MM
        r"(\d{1,2})\.(\d{1,2})", # MM.DD or DD.MM
    ]
    
    for pattern in date_patterns:
        date_match = re.search(pattern, text)
        if date_match:
            month, day = int(date_match.group(1)), int(date_match.group(2))
            # Assume current year
            try:
                base = now.replace(month=month, day=day)
                # If the date has already passed this year, assume next year
                if base < now:
                    base = base.replace(year=base.year + 1)
            except ValueError:
                # Invalid date, skip
                continue
            break

    # time like 5 pm, 17:30, 8:00 am, 8:30, 8am, 5pm
    hour = 9
    minute = 0
    time_patterns = [
        r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)",  # 5:30 pm, 8am
        r"(\d{1,2})(?::(\d{2}))?(?!\s*(am|pm))",  # 17:30, 8:30 (24-hour format)
    ]
    
    for pattern in time_patterns:
        time_match = re.search(pattern, text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            meridiem = (time_match.group(3) or "").lower()
            if meridiem:
                if meridiem == "pm" and hour < 12:
                    hour += 12
                if meridiem == "am" and hour == 12:
                    hour = 0
            break

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
    """Add a new task with enhanced error handling"""
    try:
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
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
    except Exception as e:
        print(f"Error adding task: {e}")
        raise


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
        except Exception:
            pass
    return result


def mark_completed(title_query: str) -> Optional[Dict]:
    """Mark a task as completed with enhanced error handling"""
    try:
        if not title_query or not title_query.strip():
            return None
            
        tasks = _load_tasks()
        for t in tasks:
            if t["title"].lower() == title_query.lower() and not t.get("completed"):
                t["completed"] = True
                t["completed_at"] = datetime.now().isoformat()
                _save_tasks(tasks)
                return t
        return None
    except Exception as e:
        print(f"Error marking task as completed: {e}")
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


def delete_task(title_query: str) -> Optional[Dict]:
    """Delete a task by title"""
    tasks = _load_tasks()
    for i, t in enumerate(tasks):
        if t["title"].lower() == title_query.lower():
            deleted_task = tasks.pop(i)
            _save_tasks(tasks)
            return deleted_task
    return None


def search_tasks(search_query: str) -> List[Dict]:
    """Search tasks by title or description"""
    tasks = _load_tasks()
    query_lower = search_query.lower()
    return [t for t in tasks if query_lower in t["title"].lower()]


def get_all_tasks() -> List[Dict]:
    """Get all tasks (completed and pending)"""
    return _load_tasks()


def get_task_statistics() -> Dict:
    """Get task statistics for productivity insights"""
    tasks = _load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.get("completed"))
    pending = total - completed
    overdue = len(overdue_tasks())
    
    # Priority breakdown
    high_priority = sum(1 for t in tasks if t.get("priority") == "high" and not t.get("completed"))
    normal_priority = sum(1 for t in tasks if t.get("priority") == "normal" and not t.get("completed"))
    low_priority = sum(1 for t in tasks if t.get("priority") == "low" and not t.get("completed"))
    
    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "overdue_tasks": overdue,
        "completion_rate": (completed / total * 100) if total > 0 else 0,
        "high_priority_pending": high_priority,
        "normal_priority_pending": normal_priority,
        "low_priority_pending": low_priority
    }


def add_category(title_query: str, category: str) -> Optional[Dict]:
    """Add a category to a task"""
    tasks = _load_tasks()
    for t in tasks:
        if t["title"].lower() == title_query.lower():
            t["category"] = category.strip().lower()
            _save_tasks(tasks)
            return t
    return None


def get_tasks_by_category(category: str) -> List[Dict]:
    """Get tasks filtered by category"""
    tasks = _load_tasks()
    return [t for t in tasks if t.get("category", "").lower() == category.lower()]


def get_categories() -> List[str]:
    """Get all unique categories"""
    tasks = _load_tasks()
    categories = set()
    for t in tasks:
        if "category" in t and t["category"]:
            categories.add(t["category"])
    return sorted(list(categories))


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
    if period == "all":
        items = get_all_tasks()
        if not items:
            return "You have no tasks."
        return "All tasks: " + "; ".join(format_task(t) for t in items[:10])
    return ""


def format_statistics(stats: Dict) -> str:
    """Format task statistics for voice output"""
    completion_rate = round(stats["completion_rate"], 1)
    return f"""Task Statistics:
    Total tasks: {stats['total_tasks']}
    Completed: {stats['completed_tasks']}
    Pending: {stats['pending_tasks']}
    Overdue: {stats['overdue_tasks']}
    Completion rate: {completion_rate}%
    High priority pending: {stats['high_priority_pending']}
    Normal priority pending: {stats['normal_priority_pending']}
    Low priority pending: {stats['low_priority_pending']}"""


def set_task_reminder(title_query: str, reminder_minutes: int = 30) -> Optional[Dict]:
    """Set a reminder for a task"""
    tasks = _load_tasks()
    for t in tasks:
        if t["title"].lower() == title_query.lower() and not t.get("completed"):
            # Add reminder info to task
            t["reminder_minutes"] = reminder_minutes
            t["reminder_set"] = True
            _save_tasks(tasks)
            return t
    return None


def get_tasks_needing_reminders() -> List[Dict]:
    """Get tasks that need reminders based on their deadlines"""
    tasks = _load_tasks()
    now = datetime.now()
    tasks_needing_reminders = []
    
    for t in tasks:
        if t.get("completed") or not t.get("deadline"):
            continue
            
        try:
            deadline = datetime.fromisoformat(t["deadline"])
            time_until_deadline = deadline - now
            
            # If task is due within the next hour and no reminder has been set
            if (0 < time_until_deadline.total_seconds() <= 3600 and 
                not t.get("reminder_set")):
                tasks_needing_reminders.append(t)
        except Exception:
            continue
    
    return tasks_needing_reminders


def get_daily_task_summary() -> str:
    """Get a comprehensive daily task summary"""
    today_tasks = list_tasks("today")
    overdue_tasks_list = overdue_tasks()
    stats = get_task_statistics()
    
    summary = f"Daily Task Summary:\n"
    summary += f"You have {len(today_tasks)} tasks for today.\n"
    
    if overdue_tasks_list:
        summary += f"You have {len(overdue_tasks_list)} overdue tasks.\n"
    
    if today_tasks:
        summary += "Today's tasks:\n"
        for i, task in enumerate(today_tasks[:5], 1):
            priority_emoji = {"high": "🔴", "normal": "🟡", "low": "🟢"}.get(task.get("priority", "normal"), "🟡")
            summary += f"{i}. {priority_emoji} {task['title']}\n"
    
    summary += f"\nOverall: {stats['completed_tasks']} completed, {stats['pending_tasks']} pending"
    return summary


def get_task_help() -> str:
    """Get help information for task management commands"""
    help_text = """Task Management Commands:

Adding Tasks:
- "Add task: [description]"
- "Add urgent task: [description]"
- "Create task: [description] by [deadline]"
- "New task: [description] at [time]"

Managing Tasks:
- "What are my tasks today?"
- "Show today's tasks"
- "What are my tasks this week?"
- "Show overdue tasks"
- "List all tasks"

Completing Tasks:
- "Mark task completed: [task name]"
- "Complete task: [task name]"
- "Finish task: [task name]"

Task Organization:
- "Set task priority: [task name] to [high/normal/low]"
- "Add task category: [task name] to [category]"
- "Show tasks by category: [category]"
- "List categories"

Searching and Statistics:
- "Search tasks: [search term]"
- "Find task: [search term]"
- "Task statistics"
- "Daily summary"

Deleting Tasks:
- "Delete task: [task name]"

Reminders:
- "Set task reminder: [task name] in [X] minutes"
- "What tasks need reminders?"

Deadline Examples:
- "by 5 PM today"
- "before Friday"
- "at 2:30 PM tomorrow"
- "on Monday"
- "next week"
- "this weekend"
"""
    return help_text
