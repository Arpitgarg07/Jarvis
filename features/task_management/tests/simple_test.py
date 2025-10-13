"""
Simple Test Script for Task Management System
============================================

This script tests the basic functionality without Unicode characters.
"""

import os
import sys
from datetime import datetime

# Import our task management modules
try:
    import os
    import sys

    # Add the parent directory to the path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from jarvis_task_integration import JarvisTaskIntegration
    from task_config import setup_directories
    from task_manager import Priority, TaskManager, TaskVoiceInterface

    print("All modules imported successfully!")
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure all files are in the same directory:")
    print("- task_manager.py")
    print("- jarvis_task_integration.py")
    print("- task_config.py")
    sys.exit(1)


def test_basic_functionality():
    """Test basic task management functionality"""
    print("\nTesting Basic Functionality...")
    print("=" * 40)

    # Initialize task manager
    task_manager = TaskManager("test_tasks.json")

    # Test adding tasks
    print("1. Testing task creation...")
    task_id1 = task_manager.add_task(
        "Test task 1", "This is a test task", Priority.NORMAL
    )
    task_id2 = task_manager.add_task(
        "Urgent test task", "This is urgent", Priority.URGENT
    )
    print(f"   Created tasks: {task_id1}, {task_id2}")

    # Test task retrieval
    print("2. Testing task retrieval...")
    pending_tasks = task_manager.get_pending_tasks()
    print(f"   Found {len(pending_tasks)} pending tasks")

    # Test task completion
    print("3. Testing task completion...")
    success = task_manager.complete_task(task_id1)
    print(f"   Task completion: {'Success' if success else 'Failed'}")

    # Test task summary
    print("4. Testing task summary...")
    summary = task_manager.get_task_summary()
    print(
        f"   Summary: {summary['pending_tasks']} pending, {summary['completed_tasks']} completed"
    )

    # Clean up test file
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
        print("   Cleaned up test file")


def test_voice_commands():
    """Test voice command parsing"""
    print("\nTesting Voice Commands...")
    print("=" * 40)

    voice_interface = TaskVoiceInterface()

    test_commands = [
        "Add task: Buy groceries",
        "Add urgent task: Submit assignment by Friday",
        "What are my tasks today?",
        "Task summary",
    ]

    for i, command in enumerate(test_commands, 1):
        print(f"{i}. Testing: '{command}'")
        try:
            response = voice_interface.process_voice_command(command)
            print(f"   Response: {response[:50]}{'...' if len(response) > 50 else ''}")
        except Exception as e:
            print(f"   Error: {e}")


def test_integration():
    """Test Jarvis integration"""
    print("\nTesting Jarvis Integration...")
    print("=" * 40)

    integration = JarvisTaskIntegration()

    # Test command detection
    test_commands = [
        ("Add task: Test task", True),
        ("What time is it?", False),
        ("Task summary", True),
        ("Hello Jarvis", False),
    ]

    for command, expected in test_commands:
        is_task_command = integration.is_task_command(command)
        status = "PASS" if is_task_command == expected else "FAIL"
        print(f"{status} '{command}' -> Task command: {is_task_command}")


def show_usage_examples():
    """Show usage examples"""
    print("\nUsage Examples...")
    print("=" * 40)

    examples = [
        "Add task: Buy groceries",
        "Add urgent task: Submit assignment by Friday",
        "Add task: Call mom by 5 PM today",
        "What are my tasks today?",
        "What are my tasks this week?",
        "Mark task completed: Buy groceries",
        "Set task priority: Call mom to high",
        "Show overdue tasks",
        "Task summary",
    ]

    print("Voice Commands you can use:")
    for i, example in enumerate(examples, 1):
        print(f"{i:2}. {example}")


def main():
    """Main test function"""
    print("Voice-Controlled Task Management System - Setup & Test")
    print("=" * 60)

    # Setup directories
    setup_directories()

    # Run tests
    test_basic_functionality()
    test_voice_commands()
    test_integration()
    show_usage_examples()

    print("\nAll tests completed!")
    print("\nNext steps:")
    print("1. Integrate with your existing Jarvis system")
    print("2. Test with your microphone and speakers")
    print("3. Customize voice commands in task_config.py")
    print("4. Set up automatic reminders if needed")

    print("\nFiles created:")
    print("- task_manager.py (Core task management)")
    print("- jarvis_task_integration.py (Jarvis integration)")
    print("- jarvis_with_tasks.py (Complete example)")
    print("- task_config.py (Configuration)")
    print("- tasks.json (Task data storage)")


if __name__ == "__main__":
    main()
