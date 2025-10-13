"""
Jarvis Task Management Integration Example
==========================================

This file shows how to integrate the voice-controlled task management system
with your existing Jarvis AI assistant.

Copy the relevant parts to your main Jarvis file.
"""

import threading
import time

import pyttsx3
import speech_recognition as sr
from jarvis_task_integration import JarvisTaskIntegration


class JarvisWithTaskManagement:
    """Enhanced Jarvis with task management capabilities"""

    def __init__(self):
        # Initialize speech recognition and TTS
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()

        # Initialize task management
        self.task_integration = JarvisTaskIntegration(self)

        # Setup voice settings
        self.setup_voice()

        # Task management settings
        self.task_reminders_enabled = True
        self.reminder_interval = 3600  # 1 hour in seconds

        print("Jarvis with Task Management initialized!")
        print("Available task commands:")
        print("- Add task: [task description]")
        print("- Add urgent task: [task description]")
        print("- Mark task completed: [task name]")
        print("- What are my tasks today?")
        print("- What are my tasks this week?")
        print("- Show overdue tasks")
        print("- Task summary")
        print("- Set task priority: [task name] to [high/normal/low/urgent]")

    def setup_voice(self):
        """Setup voice settings"""
        voices = self.tts_engine.getProperty("voices")
        if voices:
            self.tts_engine.setProperty("voice", voices[0].id)
        self.tts_engine.setProperty("rate", 150)
        self.tts_engine.setProperty("volume", 0.8)

    def speak(self, text):
        """Speak text using TTS"""
        print(f"Jarvis: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def listen(self):
        """Listen for voice commands"""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=5)

        try:
            command = self.recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results: {e}"

    def process_command(self, command):
        """Process voice commands"""
        if not command or command == "Could not understand audio":
            return "I didn't catch that. Please try again."

        # Check if it's a task management command
        if self.task_integration.is_task_command(command):
            response = self.task_integration.process_task_command(command)
            return response

        # Handle other Jarvis commands
        elif "hello" in command or "hi" in command:
            return "Hello! How can I help you today?"

        elif "time" in command:
            current_time = time.strftime("%H:%M")
            return f"The current time is {current_time}"

        elif "date" in command:
            current_date = time.strftime("%B %d, %Y")
            return f"Today is {current_date}"

        elif "weather" in command:
            return "I don't have weather information configured yet."

        elif "goodbye" in command or "exit" in command or "quit" in command:
            return "Goodbye! Have a great day!"

        else:
            return "I'm not sure how to help with that. Try asking about tasks, time, or date."

    def start_task_reminders(self):
        """Start background task reminder system"""

        def reminder_loop():
            while self.task_reminders_enabled:
                try:
                    notifications = self.task_integration.get_task_notifications()
                    if notifications:
                        for notification in notifications:
                            self.speak(notification)
                            time.sleep(2)  # Pause between notifications

                    time.sleep(self.reminder_interval)
                except Exception as e:
                    print(f"Error in reminder loop: {e}")
                    time.sleep(60)  # Wait 1 minute before retrying

        reminder_thread = threading.Thread(target=reminder_loop, daemon=True)
        reminder_thread.start()
        print("Task reminder system started")

    def run(self):
        """Main Jarvis loop"""
        self.speak(
            "Hello! I'm Jarvis with task management capabilities. How can I help you?"
        )

        # Start task reminders
        self.start_task_reminders()

        # Give daily task reminder
        daily_reminder = self.task_integration.get_daily_task_reminder()
        self.speak(daily_reminder)

        while True:
            try:
                command = self.listen()

                if command == "goodbye" or command == "exit" or command == "quit":
                    self.speak("Goodbye! Have a great day!")
                    break

                response = self.process_command(command)
                self.speak(response)

            except KeyboardInterrupt:
                self.speak("Goodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
                self.speak("Sorry, I encountered an error. Please try again.")


# Example of how to add task management to existing Jarvis
def add_task_management_to_existing_jarvis(existing_jarvis):
    """
    Add task management to your existing Jarvis instance

    Usage:
    add_task_management_to_existing_jarvis(your_jarvis_instance)
    """

    # Initialize task integration
    task_integration = JarvisTaskIntegration(existing_jarvis)

    # Store original process_command method
    original_process_command = existing_jarvis.process_command

    def enhanced_process_command(command):
        # Check for task commands first
        if task_integration.is_task_command(command):
            return task_integration.process_task_command(command)

        # Use original command processing
        return original_process_command(command)

    # Replace the process_command method
    existing_jarvis.process_command = enhanced_process_command
    existing_jarvis.task_integration = task_integration

    # Add task management methods
    existing_jarvis.get_task_notifications = task_integration.get_task_notifications
    existing_jarvis.get_daily_task_reminder = task_integration.get_daily_task_reminder
    existing_jarvis.export_tasks = task_integration.export_tasks_to_json
    existing_jarvis.import_tasks = task_integration.import_tasks_from_json

    print("Task management successfully added to Jarvis!")
    return task_integration


# Quick setup function
def quick_setup():
    """Quick setup for testing task management"""
    print("Setting up Jarvis with Task Management...")

    # Create new Jarvis instance
    jarvis = JarvisWithTaskManagement()

    # Test some commands
    test_commands = [
        "Add task: Buy groceries",
        "Add urgent task: Submit assignment by Friday",
        "What are my tasks today?",
        "Task summary",
    ]

    print("\nTesting task management commands:")
    for command in test_commands:
        print(f"\nTesting: {command}")
        response = jarvis.process_command(command)
        print(f"Response: {response}")

    return jarvis


if __name__ == "__main__":
    # Run the enhanced Jarvis
    jarvis = JarvisWithTaskManagement()
    jarvis.run()
