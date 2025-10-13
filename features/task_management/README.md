# Task Management Feature for Jarvis AI Assistant

A comprehensive voice-controlled task management system with bilingual support (English and Kannada).

## 🚀 Features

- **Voice Commands**: Natural language task management
- **Bilingual Support**: English and Kannada voice commands
- **Persistent Storage**: JSON-based task storage
- **Priority System**: Urgent, High, Normal, Low priorities
- **Deadline Management**: Automatic date/time parsing
- **Task Tracking**: Completion and overdue detection
- **Summaries**: Daily and weekly task overviews

## 📁 Structure

```
task_management/
├── __init__.py                 # Module initialization
├── task_manager.py            # Core task management logic
├── kannada_support.py         # Kannada language support
├── jarvis_task_integration.py # Jarvis integration
├── task_config.py             # Configuration settings
├── jarvis_with_tasks.py       # Complete example
├── tests/                     # Test files
│   ├── simple_test.py
│   ├── kannada_final_test.py
│   └── setup_and_test.py
└── docs/                      # Documentation
    ├── TASK_MANAGEMENT_README.md
    ├── KANNADA_SUPPORT_SUMMARY.md
    └── SOLUTION_SUMMARY.md
```

## 🎤 Voice Commands

### English Commands
- `Add task: [description]`
- `Add urgent task: [description]`
- `What are my tasks today?`
- `Mark task completed: [task name]`
- `Task summary`

### Kannada Commands
- `ಕಾರ್ಯ ಸೇರಿಸಿ: [description]`
- `ತುರ್ತು ಕಾರ್ಯ ಸೇರಿಸಿ: [description]`
- `ಇಂದಿನ ಕಾರ್ಯಗಳು ಯಾವುವು`
- `ಕಾರ್ಯ ಪೂರ್ಣಗೊಳಿಸಿ: [task name]`
- `ಕಾರ್ಯ ಸಾರಾಂಶ`

## 🔧 Integration

### Basic Usage
```python
from features.task_management import TaskVoiceInterface

# Initialize task management
task_interface = TaskVoiceInterface()

# Process voice commands
response = task_interface.process_voice_command("Add task: Buy groceries")
```

### Jarvis Integration
```python
from features.task_management import JarvisTaskIntegration

# Add to existing Jarvis
task_integration = JarvisTaskIntegration(your_jarvis_instance)
```

## 🧪 Testing

Run the test suite:
```bash
python -m features.task_management.tests.simple_test
python -m features.task_management.tests.kannada_final_test
```

## 📊 Data Storage

Tasks are stored in `data/tasks.json` with the following structure:
```json
{
  "id": "task_1_1703123456",
  "title": "Task title",
  "description": "Task description",
  "priority": "normal",
  "deadline": "2024-12-31 18:00",
  "created_at": "2024-12-20T10:30:00",
  "completed": false,
  "completed_at": null,
  "tags": []
}
```

## 🌐 Language Support

The system automatically detects the language of voice commands and responds accordingly:
- **English commands** → English responses
- **Kannada commands** → Kannada responses
- **Mixed commands** → Appropriate language responses

## 📝 Configuration

Edit `task_config.py` to customize:
- Voice recognition settings
- Task management preferences
- Notification settings
- Language-specific configurations

## 🤝 Contributing

This feature is part of the Jarvis AI Assistant project. See the main project documentation for contribution guidelines.

## 📄 License

This feature follows the same license as the main Jarvis project.
