# Voice-Controlled Task Management System for Jarvis

A complete voice-controlled task management system that integrates seamlessly with your existing Jarvis AI assistant. This system allows you to manage tasks using natural voice commands with persistent storage and intelligent reminders.

## 🚀 Features

### Core Functionality
- ✅ **Voice Command Processing** - Natural language task management
- ✅ **Persistent Storage** - JSON-based task storage
- ✅ **Priority System** - Urgent, High, Normal, Low priorities
- ✅ **Deadline Management** - Automatic date/time parsing
- ✅ **Task Completion Tracking** - Mark tasks as done
- ✅ **Overdue Detection** - Automatic overdue task identification
- ✅ **Task Summaries** - Daily and weekly task overviews

### Voice Commands
- **Adding Tasks**: "Add task: Buy groceries", "Add urgent task: Submit assignment by Friday"
- **Managing Tasks**: "What are my tasks today?", "Mark task completed: Buy groceries"
- **Priority Management**: "Set task priority: Call mom to high"
- **Task Overview**: "Show overdue tasks", "Task summary"

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `task_manager.py` | Core task management logic and data structures |
| `jarvis_task_integration.py` | Integration with existing Jarvis system |
| `jarvis_with_tasks.py` | Complete example implementation |
| `task_config.py` | Configuration and settings |
| `setup_and_test.py` | Setup and testing script |
| `tasks.json` | Task data storage (created automatically) |

## 🛠️ Installation & Setup

### Prerequisites
```bash
pip install speechrecognition pyttsx3
```

### Quick Setup
1. **Download all files** to your Jarvis project directory
2. **Run the setup script**:
   ```bash
   python setup_and_test.py
   ```
3. **Test the system** to ensure everything works

### Integration with Existing Jarvis

#### Method 1: Add to Existing Jarvis Class
```python
from jarvis_task_integration import JarvisTaskIntegration

# In your Jarvis class __init__ method:
self.task_integration = JarvisTaskIntegration(self)

# In your command processing method:
def process_command(self, command):
    # Check for task commands first
    if self.task_integration.is_task_command(command):
        return self.task_integration.process_task_command(command)
    
    # Process other commands normally
    return self.original_process_command(command)
```

#### Method 2: Use the Complete Example
```python
from jarvis_with_tasks import JarvisWithTaskManagement

# Create enhanced Jarvis instance
jarvis = JarvisWithTaskManagement()
jarvis.run()
```

## 🎤 Voice Commands Reference

### Adding Tasks
| Command | Example | Description |
|---------|---------|-------------|
| `Add task: [description]` | "Add task: Buy groceries" | Create normal priority task |
| `Add urgent task: [description]` | "Add urgent task: Submit assignment by Friday" | Create urgent priority task |
| `Add task: [description] by [time]` | "Add task: Call mom by 5 PM today" | Create task with deadline |

### Managing Tasks
| Command | Example | Description |
|---------|---------|-------------|
| `What are my tasks today?` | "What are my tasks today?" | Show today's tasks |
| `What are my tasks this week?` | "What are my tasks this week?" | Show this week's tasks |
| `Mark task completed: [name]` | "Mark task completed: Buy groceries" | Complete a task |
| `Set task priority: [name] to [level]` | "Set task priority: Call mom to high" | Change task priority |

### Task Overview
| Command | Example | Description |
|---------|---------|-------------|
| `Show overdue tasks` | "Show overdue tasks" | List overdue tasks |
| `Task summary` | "Task summary" | Complete task overview |

## 🔧 Configuration

Edit `task_config.py` to customize:

### Voice Settings
```python
VOICE_TIMEOUT = 5  # seconds
TTS_RATE = 150  # words per minute
TTS_VOLUME = 0.8  # 0.0 to 1.0
```

### Task Settings
```python
DEFAULT_PRIORITY = "normal"
AUTO_REMINDER_INTERVAL = 3600  # 1 hour
DAILY_REMINDER_TIME = time(9, 0)  # 9:00 AM
```

### Custom Voice Commands
Add your own command patterns:
```python
TASK_COMMAND_PATTERNS = {
    'add_task': [
        r'add task:?\s*(.+)',
        r'create task:?\s*(.+)',
        r'new task:?\s*(.+)',
        r'todo:?\s*(.+)'
    ],
    # Add more patterns...
}
```

## 📊 Task Data Structure

Tasks are stored in JSON format with the following structure:
```json
{
  "id": "task_1_1703123456",
  "title": "Buy groceries",
  "description": "",
  "priority": "normal",
  "deadline": "2024-12-31 18:00",
  "created_at": "2024-12-20T10:30:00",
  "completed": false,
  "completed_at": null,
  "tags": []
}
```

## 🔄 Priority Levels

| Priority | Description | Color |
|----------|-------------|-------|
| `urgent` | Critical tasks requiring immediate attention | Red |
| `high` | Important tasks with high priority | Orange |
| `normal` | Regular tasks (default) | Green |
| `low` | Low priority tasks | Gray |

## 📅 Date/Time Parsing

The system automatically parses various date/time formats:

### Supported Formats
- **Today/Tomorrow**: "by 5 PM today", "due tomorrow"
- **Day Names**: "by Friday", "due Monday"
- **Dates**: "by 12/25", "due 12/31/2024"
- **Times**: "by 5 PM", "due 18:00"

### Examples
```
"Add task: Call mom by 5 PM today"
"Add urgent task: Submit assignment by Friday"
"Add task: Buy groceries by 12/25"
```

## 🔔 Notifications & Reminders

### Automatic Notifications
- **Overdue Tasks**: Alerts for tasks past their deadline
- **Daily Reminders**: Morning task summary
- **Priority Alerts**: Notifications for urgent tasks

### Customization
```python
# Enable/disable notifications
ENABLE_OVERDUE_NOTIFICATIONS = True
ENABLE_DAILY_REMINDERS = True
ENABLE_PRIORITY_NOTIFICATIONS = True
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python setup_and_test.py
```

This will test:
- ✅ Basic task management functionality
- ✅ Voice command parsing
- ✅ Jarvis integration
- ✅ Data persistence
- ✅ Date/time handling

## 📈 Advanced Features

### Task Export/Import
```python
# Export tasks to JSON
integration.export_tasks_to_json("backup_tasks.json")

# Import tasks from JSON
integration.import_tasks_from_json("backup_tasks.json")
```

### Task Notifications
```python
# Get current notifications
notifications = integration.get_task_notifications()

# Get daily reminder
reminder = integration.get_daily_task_reminder()
```

### Task Search
```python
# Search tasks by keyword
tasks = task_manager.search_tasks("groceries")
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all files are in the same directory
   - Check Python version compatibility (3.7+)

2. **Voice Recognition Issues**
   - Check microphone permissions
   - Adjust `VOICE_ENERGY_THRESHOLD` in config
   - Test with `python setup_and_test.py`

3. **TTS Issues**
   - Install additional voices if needed
   - Adjust `TTS_RATE` and `TTS_VOLUME` settings

4. **File Permission Errors**
   - Ensure write permissions for task storage
   - Check directory creation permissions

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

To add new features or improve existing ones:

1. **Add new voice commands** in `task_config.py`
2. **Extend task data structure** in `task_manager.py`
3. **Add new integration methods** in `jarvis_task_integration.py`
4. **Update tests** in `setup_and_test.py`

## 📝 License

This project is part of your Jarvis AI assistant system. Use and modify as needed for your personal use.

## 🎯 Future Enhancements

Potential improvements:
- 📱 Mobile app integration
- 🌐 Web dashboard
- 📧 Email notifications
- 🔗 Calendar integration
- 📊 Task analytics and reports
- 🏷️ Task categories and tags
- 👥 Team task sharing

---

**Happy Task Managing! 🚀**

Your voice-controlled task management system is now ready to help you stay organized and productive!
