"""
Task Management Feature for Jarvis AI Assistant
==============================================

This module provides voice-controlled task management capabilities with support
for both English and Kannada languages.

Features:
- Voice-controlled task creation and management
- Persistent JSON storage
- Priority system (urgent, high, normal, low)
- Deadline parsing and overdue detection
- Daily/weekly task summaries
- Bilingual support (English and Kannada)
- Seamless Jarvis integration

Usage:
    from features.task_management import TaskVoiceInterface
    
    # Initialize task management
    task_interface = TaskVoiceInterface()
    
    # Process voice commands
    response = task_interface.process_voice_command("Add task: Buy groceries")
"""

from .task_manager import TaskVoiceInterface, TaskManager, Priority
from .kannada_support import KannadaVoiceProcessor, Language
from .jarvis_task_integration import JarvisTaskIntegration

__version__ = "1.0.0"
__author__ = "Jarvis AI Assistant"
__description__ = "Voice-controlled task management with bilingual support"

__all__ = [
    'TaskVoiceInterface',
    'TaskManager', 
    'Priority',
    'KannadaVoiceProcessor',
    'Language',
    'JarvisTaskIntegration'
]
