"""
Jarvis Task Management Integration
=================================

This module integrates the voice-controlled task management system
with your existing Jarvis AI assistant.

Usage:
1. Import this module in your main Jarvis file
2. Add task management commands to your voice recognition system
3. The system will automatically handle task operations via voice commands
"""

import json
import os
from datetime import datetime

from task_manager import Priority, TaskManager, TaskVoiceInterface


class JarvisTaskIntegration:
    """Integration class for Jarvis AI assistant"""

    def __init__(self, jarvis_instance=None):
        self.task_interface = TaskVoiceInterface()
        self.jarvis = jarvis_instance
        self.setup_task_commands()

    def setup_task_commands(self):
        """Setup task management commands for Jarvis"""
        self.task_commands = {
            "add_task": self.handle_add_task,
            "complete_task": self.handle_complete_task,
            "show_tasks": self.handle_show_tasks,
            "task_summary": self.handle_task_summary,
            "set_priority": self.handle_set_priority,
            "overdue_tasks": self.handle_overdue_tasks,
        }

    def is_task_command(self, command: str) -> bool:
        """Check if the command is related to task management"""
        task_keywords = [
            "task",
            "todo",
            "add task",
            "complete task",
            "mark task",
            "priority",
            "deadline",
            "overdue",
            "summary",
            "tasks today",
            "tasks this week",
            "urgent task",
        ]

        command_lower = command.lower()
        return any(keyword in command_lower for keyword in task_keywords)

    def process_task_command(self, command: str) -> str:
        """Process task management commands"""
        try:
            response = self.task_interface.process_voice_command(command)
            return response
        except Exception as e:
            return f"Error processing task command: {str(e)}"

    def handle_add_task(self, command: str) -> str:
        """Handle adding new tasks"""
        return self.process_task_command(command)

    def handle_complete_task(self, command: str) -> str:
        """Handle completing tasks"""
        return self.process_task_command(command)

    def handle_show_tasks(self, command: str) -> str:
        """Handle showing tasks"""
        return self.process_task_command(command)

    def handle_task_summary(self, command: str) -> str:
        """Handle task summary requests"""
        return self.process_task_command(command)

    def handle_set_priority(self, command: str) -> str:
        """Handle setting task priority"""
        return self.process_task_command(command)

    def handle_overdue_tasks(self, command: str) -> str:
        """Handle overdue task requests"""
        return self.process_task_command(command)

    def get_task_notifications(self) -> list:
        """Get task notifications for Jarvis to announce"""
        notifications = []

        # Check for overdue tasks
        overdue_tasks = self.task_interface.task_manager.get_overdue_tasks()
        if overdue_tasks:
            notifications.append(f"You have {len(overdue_tasks)} overdue tasks!")

        # Check for tasks due today
        today_tasks = self.task_interface.task_manager.get_tasks_by_date()
        if today_tasks:
            notifications.append(f"You have {len(today_tasks)} tasks due today")

        # Check for urgent tasks
        urgent_tasks = self.task_interface.task_manager.get_tasks_by_priority(
            Priority.URGENT
        )
        if urgent_tasks:
            notifications.append(f"You have {len(urgent_tasks)} urgent tasks pending")

        return notifications

    def get_daily_task_reminder(self) -> str:
        """Get daily task reminder message"""
        summary = self.task_interface.task_manager.get_task_summary()

        if summary["tasks_today"] > 0:
            return f"Good morning! You have {summary['tasks_today']} tasks scheduled for today."
        elif summary["overdue_tasks"] > 0:
            return f"Good morning! You have {summary['overdue_tasks']} overdue tasks that need attention."
        else:
            return "Good morning! You have no tasks scheduled for today. Great job staying on top of things!"

    def export_tasks_to_json(self, filename: str = None) -> str:
        """Export tasks to JSON file"""
        if not filename:
            filename = f"tasks_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(
                    [task.__dict__ for task in self.task_interface.task_manager.tasks],
                    f,
                    indent=2,
                    ensure_ascii=False,
                    default=str,
                )
            return f"Tasks exported to {filename}"
        except Exception as e:
            return f"Error exporting tasks: {str(e)}"

    def import_tasks_from_json(self, filename: str) -> str:
        """Import tasks from JSON file"""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)

            imported_count = 0
            for task_data in data:
                self.task_interface.task_manager.add_task(
                    title=task_data["title"],
                    description=task_data.get("description", ""),
                    priority=Priority(task_data.get("priority", "normal")),
                    deadline=task_data.get("deadline"),
                    tags=task_data.get("tags", []),
                )
                imported_count += 1

            return f"Successfully imported {imported_count} tasks from {filename}"
        except Exception as e:
            return f"Error importing tasks: {str(e)}"


# Example integration with Jarvis
def integrate_with_jarvis(jarvis_instance):
    """
    Example function showing how to integrate task management with Jarvis

    Add this to your main Jarvis file:

    from jarvis_task_integration import JarvisTaskIntegration

    # Initialize task management
    task_integration = JarvisTaskIntegration(jarvis_instance)

    # In your voice recognition loop:
    if task_integration.is_task_command(user_command):
        response = task_integration.process_task_command(user_command)
        jarvis_instance.speak(response)
    """

    task_integration = JarvisTaskIntegration(jarvis_instance)

    # Add task management to Jarvis's command processing
    def enhanced_process_command(self, command):
        # Check if it's a task command first
        if task_integration.is_task_command(command):
            return task_integration.process_task_command(command)

        # Process other Jarvis commands normally
        return self.original_process_command(command)

    # Monkey patch the process command method
    jarvis_instance.original_process_command = jarvis_instance.process_command
    jarvis_instance.process_command = enhanced_process_command.__get__(
        jarvis_instance, jarvis_instance.__class__
    )

    return task_integration


# Example usage
if __name__ == "__main__":
    # Test the integration
    integration = JarvisTaskIntegration()

    # Test commands
    test_commands = [
        "Add task: Buy groceries",
        "Add urgent task: Submit assignment by Friday",
        "What are my tasks today?",
        "Task summary",
        "Show overdue tasks",
    ]

    print("Testing Jarvis Task Integration")
    print("=" * 40)

    for command in test_commands:
        print(f"\nCommand: {command}")
        if integration.is_task_command(command):
            response = integration.process_task_command(command)
            print(f"Jarvis Response: {response}")
        else:
            print("Not a task command")
