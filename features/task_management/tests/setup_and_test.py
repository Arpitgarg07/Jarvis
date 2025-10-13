"""
Task Management Setup and Test Script
====================================

This script helps you set up and test the voice-controlled task management system.
Run this script to verify everything is working correctly.
"""

import os
import sys
from datetime import datetime, timedelta

# Import our task management modules
try:
    import sys
    import os

    # Add the parent directory to the path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from task_manager import TaskVoiceInterface, TaskManager, Priority
    from jarvis_task_integration import JarvisTaskIntegration
    from task_config import setup_directories

    print("✓ All modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all files are in the same directory:")
    print("- task_manager.py")
    print("- jarvis_task_integration.py")
    print("- task_config.py")
    sys.exit(1)


def test_basic_functionality():
    """Test basic task management functionality"""
    print("\n🧪 Testing Basic Functionality...")
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
    print(f"   ✅ Created tasks: {task_id1}, {task_id2}")

    # Test task retrieval
    print("2. Testing task retrieval...")
    pending_tasks = task_manager.get_pending_tasks()
    print(f"   ✅ Found {len(pending_tasks)} pending tasks")

    # Test task completion
    print("3. Testing task completion...")
    success = task_manager.complete_task(task_id1)
    print(f"   ✅ Task completion: {'Success' if success else 'Failed'}")

    # Test task summary
    print("4. Testing task summary...")
    summary = task_manager.get_task_summary()
    print(
        f"   ✅ Summary: {summary['pending_tasks']} pending, {summary['completed_tasks']} completed"
    )

    # Clean up test file
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")
        print("   ✅ Cleaned up test file")


def test_voice_commands():
    """Test voice command parsing"""
    print("\n🎤 Testing Voice Commands...")
    print("=" * 40)

    voice_interface = TaskVoiceInterface()

    test_commands = [
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

    for i, command in enumerate(test_commands, 1):
        print(f"{i}. Testing: '{command}'")
        try:
            response = voice_interface.process_voice_command(command)
            print(
                f"   ✅ Response: {response[:50]}{'...' if len(response) > 50 else ''}"
            )
        except Exception as e:
            print(f"   ❌ Error: {e}")


def test_integration():
    """Test Jarvis integration"""
    print("\n🤖 Testing Jarvis Integration...")
    print("=" * 40)

    integration = JarvisTaskIntegration()

    # Test command detection
    test_commands = [
        ("Add task: Test task", True),
        ("What time is it?", False),
        ("Task summary", True),
        ("Hello Jarvis", False),
        ("Show overdue tasks", True),
    ]

    for command, expected in test_commands:
        is_task_command = integration.is_task_command(command)
        status = "✅" if is_task_command == expected else "❌"
        print(f"{status} '{command}' -> Task command: {is_task_command}")


def test_data_persistence():
    """Test data persistence"""
    print("\n💾 Testing Data Persistence...")
    print("=" * 40)

    # Create tasks
    task_manager1 = TaskManager("persistence_test.json")
    task_manager1.add_task("Persistent task 1", priority=Priority.HIGH)
    task_manager1.add_task("Persistent task 2", priority=Priority.NORMAL)

    # Create new instance (simulates restart)
    task_manager2 = TaskManager("persistence_test.json")

    # Check if tasks were loaded
    tasks = task_manager2.get_pending_tasks()
    print(f"✅ Loaded {len(tasks)} tasks from file")

    # Clean up
    if os.path.exists("persistence_test.json"):
        os.remove("persistence_test.json")


def test_date_handling():
    """Test date and time handling"""
    print("\n📅 Testing Date/Time Handling...")
    print("=" * 40)

    task_manager = TaskManager()

    # Test different deadline formats
    test_deadlines = ["2024-12-31 23:59", "2024-12-31", "tomorrow", "friday"]

    for deadline in test_deadlines:
        try:
            task_id = task_manager.add_task(
                f"Test task with deadline {deadline}", deadline=deadline
            )
            print(f"✅ Created task with deadline: {deadline}")
        except Exception as e:
            print(f"❌ Error with deadline '{deadline}': {e}")


def show_usage_examples():
    """Show usage examples"""
    print("\n📚 Usage Examples...")
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

    print("\nIntegration with your existing Jarvis:")
    print("1. Import: from jarvis_task_integration import JarvisTaskIntegration")
    print("2. Initialize: task_integration = JarvisTaskIntegration(your_jarvis)")
    print("3. Check commands: if task_integration.is_task_command(command):")
    print("4. Process: response = task_integration.process_task_command(command)")


def main():
    """Main test function"""
    print("🚀 Voice-Controlled Task Management System - Setup & Test")
    print("=" * 60)

    # Setup directories
    setup_directories()

    # Run tests
    test_basic_functionality()
    test_voice_commands()
    test_integration()
    test_data_persistence()
    test_date_handling()
    show_usage_examples()

    print("\n🎉 All tests completed!")
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
