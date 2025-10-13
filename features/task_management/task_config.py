"""
Task Management Configuration
============================

Configuration file for the voice-controlled task management system.
Customize these settings according to your preferences.
"""

import os
from datetime import time

# File paths
TASKS_DATA_FILE = "tasks.json"
TASKS_BACKUP_DIR = "task_backups"
EXPORT_DIR = "task_exports"

# Task management settings
DEFAULT_PRIORITY = "normal"
AUTO_REMINDER_INTERVAL = 3600  # 1 hour in seconds
DAILY_REMINDER_TIME = time(9, 0)  # 9:00 AM
OVERDUE_CHECK_INTERVAL = 1800  # 30 minutes

# Voice recognition settings
VOICE_TIMEOUT = 5  # seconds
VOICE_PHRASE_TIMEOUT = 0.3  # seconds
VOICE_ENERGY_THRESHOLD = 300

# Text-to-speech settings
TTS_RATE = 150  # words per minute
TTS_VOLUME = 0.8  # 0.0 to 1.0
TTS_VOICE_INDEX = 0  # Use first available voice

# Task display settings
MAX_TASKS_DISPLAY = 10
TASK_SUMMARY_FORMAT = "detailed"  # "detailed" or "brief"

# Notification settings
ENABLE_OVERDUE_NOTIFICATIONS = True
ENABLE_DAILY_REMINDERS = True
ENABLE_PRIORITY_NOTIFICATIONS = True
NOTIFICATION_SOUND = True

# Data retention settings
KEEP_COMPLETED_TASKS_DAYS = 30  # Keep completed tasks for 30 days
AUTO_BACKUP_ENABLED = True
BACKUP_FREQUENCY_HOURS = 24  # Backup every 24 hours

# Voice command patterns (customize as needed)
TASK_COMMAND_PATTERNS = {
    "add_task": [
        r"add task:?\s*(.+)",
        r"create task:?\s*(.+)",
        r"new task:?\s*(.+)",
        r"todo:?\s*(.+)",
    ],
    "add_urgent_task": [
        r"add urgent task:?\s*(.+)",
        r"urgent task:?\s*(.+)",
        r"priority task:?\s*(.+)",
    ],
    "complete_task": [
        r"mark task completed:?\s*(.+)",
        r"complete task:?\s*(.+)",
        r"done:?\s*(.+)",
        r"finished:?\s*(.+)",
    ],
    "show_tasks_today": [
        r"what are my tasks today",
        r"tasks today",
        r"today tasks",
        r"show today tasks",
    ],
    "show_tasks_week": [
        r"what are my tasks this week",
        r"tasks this week",
        r"week tasks",
        r"show week tasks",
    ],
    "show_overdue": [
        r"show overdue tasks",
        r"overdue tasks",
        r"late tasks",
        r"missed tasks",
    ],
    "task_summary": [r"task summary", r"task overview", r"task status", r"my tasks"],
}

# Priority levels and their colors (for GUI if implemented)
PRIORITY_COLORS = {
    "urgent": "#FF0000",  # Red
    "high": "#FF8C00",  # Orange
    "normal": "#008000",  # Green
    "low": "#808080",  # Gray
}

# Date/time parsing patterns
DEADLINE_PATTERNS = [
    r"by\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+today",
    r"by\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+tomorrow",
    r"by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",
    r"by\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
    r"due\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+today",
    r"due\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+tomorrow",
    r"deadline\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)",
    r"until\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)",
]


# Create necessary directories
def setup_directories():
    """Create necessary directories for task management"""
    directories = [TASKS_BACKUP_DIR, EXPORT_DIR]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")


# Initialize configuration
if __name__ == "__main__":
    setup_directories()
    print("Task management configuration loaded successfully!")
    print(f"Tasks will be saved to: {TASKS_DATA_FILE}")
    print(f"Backups will be saved to: {TASKS_BACKUP_DIR}")
    print(f"Exports will be saved to: {EXPORT_DIR}")
