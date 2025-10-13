"""
Kannada Language Support for Task Management
===========================================

This module provides Kannada language support for the voice-controlled
task management system, including voice commands, responses, and TTS.
"""

from enum import Enum
from typing import Dict, List


class Language(Enum):
    """Supported languages"""

    ENGLISH = "en"
    KANNADA = "kn"


class KannadaTranslations:
    """Kannada translations for task management"""

    # Voice command patterns in Kannada
    KANNADA_COMMANDS = {
        "add_task": [
            r"ಕಾರ್ಯ ಸೇರಿಸಿ:?\s*(.+)",
            r"ಕೆಲಸ ಸೇರಿಸಿ:?\s*(.+)",
            r"ಟಾಸ್ಕ್ ಸೇರಿಸಿ:?\s*(.+)",
            r"ಹೊಸ ಕಾರ್ಯ:?\s*(.+)",
            r"ಹೊಸ ಕೆಲಸ:?\s*(.+)",
        ],
        "add_urgent_task": [
            r"ತುರ್ತು ಕಾರ್ಯ ಸೇರಿಸಿ:?\s*(.+)",
            r"ತುರ್ತು ಕೆಲಸ ಸೇರಿಸಿ:?\s*(.+)",
            r"ಅತ್ಯಾವಶ್ಯಕ ಕಾರ್ಯ:?\s*(.+)",
            r"ಅತ್ಯಾವಶ್ಯಕ ಕೆಲಸ:?\s*(.+)",
            r"ಅರ್ಜೆಂಟ್ ಕಾರ್ಯ:?\s*(.+)",
        ],
        "complete_task": [
            r"ಕಾರ್ಯ ಪೂರ್ಣಗೊಳಿಸಿ:?\s*(.+)",
            r"ಕೆಲಸ ಮುಗಿಸಿ:?\s*(.+)",
            r"ಕಾರ್ಯ ಮುಗಿಸಿ:?\s*(.+)",
            r"ಕೆಲಸ ಪೂರ್ಣಗೊಳಿಸಿ:?\s*(.+)",
            r"ಡನ್:?\s*(.+)",
            r"ಮುಗಿಸಿದೆ:?\s*(.+)",
        ],
        "show_tasks_today": [
            r"ಇಂದಿನ ಕಾರ್ಯಗಳು ಯಾವುವು",
            r"ಇಂದಿನ ಕೆಲಸಗಳು ಯಾವುವು",
            r"ಇಂದಿನ ಟಾಸ್ಕ್ಗಳು ಯಾವುವು",
            r"ಇಂದಿನ ಕಾರ್ಯಗಳನ್ನು ತೋರಿಸಿ",
            r"ಇಂದಿನ ಕೆಲಸಗಳನ್ನು ತೋರಿಸಿ",
        ],
        "show_tasks_week": [
            r"ಈ ವಾರದ ಕಾರ್ಯಗಳು ಯಾವುವು",
            r"ಈ ವಾರದ ಕೆಲಸಗಳು ಯಾವುವು",
            r"ಈ ವಾರದ ಟಾಸ್ಕ್ಗಳು ಯಾವುವು",
            r"ಈ ವಾರದ ಕಾರ್ಯಗಳನ್ನು ತೋರಿಸಿ",
            r"ಈ ವಾರದ ಕೆಲಸಗಳನ್ನು ತೋರಿಸಿ",
        ],
        "show_overdue": [
            r"ವಿಳಂಬವಾದ ಕಾರ್ಯಗಳನ್ನು ತೋರಿಸಿ",
            r"ವಿಳಂಬವಾದ ಕೆಲಸಗಳನ್ನು ತೋರಿಸಿ",
            r"ವಿಳಂಬವಾದ ಟಾಸ್ಕ್ಗಳನ್ನು ತೋರಿಸಿ",
            r"ಲೇಟ್ ಕಾರ್ಯಗಳು",
            r"ಮಿಸ್ ಆದ ಕಾರ್ಯಗಳು",
        ],
        "task_summary": [
            r"ಕಾರ್ಯ ಸಾರಾಂಶ",
            r"ಕೆಲಸ ಸಾರಾಂಶ",
            r"ಟಾಸ್ಕ್ ಸಾರಾಂಶ",
            r"ಕಾರ್ಯ ಅವಲೋಕನ",
            r"ಕೆಲಸ ಅವಲೋಕನ",
            r"ನನ್ನ ಕಾರ್ಯಗಳು",
            r"ನನ್ನ ಕೆಲಸಗಳು",
        ],
        "set_priority": [
            r"ಕಾರ್ಯ ಪ್ರಾಮುಖ್ಯತೆ:?\s*(.+?)\s+ಗೆ\s+(ಅತ್ಯಾವಶ್ಯಕ|ಅಧಿಕ|ಸಾಮಾನ್ಯ|ಕಡಿಮೆ)",
            r"ಕೆಲಸ ಪ್ರಾಮುಖ್ಯತೆ:?\s*(.+?)\s+ಗೆ\s+(ಅತ್ಯಾವಶ್ಯಕ|ಅಧಿಕ|ಸಾಮಾನ್ಯ|ಕಡಿಮೆ)",
            r"ಪ್ರಾಮುಖ್ಯತೆ:?\s*(.+?)\s+ಗೆ\s+(ಅತ್ಯಾವಶ್ಯಕ|ಅಧಿಕ|ಸಾಮಾನ್ಯ|ಕಡಿಮೆ)",
        ],
    }

    # Priority translations
    PRIORITY_TRANSLATIONS = {
        "urgent": "ಅತ್ಯಾವಶ್ಯಕ",
        "high": "ಅಧಿಕ",
        "normal": "ಸಾಮಾನ್ಯ",
        "low": "ಕಡಿಮೆ",
    }

    # Response messages in Kannada
    RESPONSES = {
        "task_added": "ಕಾರ್ಯ ಸೇರಿಸಲಾಗಿದೆ: {}",
        "task_completed": "ಕಾರ್ಯ ಪೂರ್ಣಗೊಂಡಿದೆ: {}",
        "task_not_found": "ಕಾರ್ಯ ಕಂಡುಬಂದಿಲ್ಲ: {}",
        "priority_updated": "ಪ್ರಾಮುಖ್ಯತೆ ನವೀಕರಿಸಲಾಗಿದೆ: {}",
        "no_tasks_today": "ಇಂದಿನ ದಿನಕ್ಕೆ ಯಾವುದೇ ಕಾರ್ಯಗಳಿಲ್ಲ",
        "no_tasks_week": "ಈ ವಾರಕ್ಕೆ ಯಾವುದೇ ಕಾರ್ಯಗಳಿಲ್ಲ",
        "no_overdue_tasks": "ಯಾವುದೇ ವಿಳಂಬವಾದ ಕಾರ್ಯಗಳಿಲ್ಲ",
        "tasks_today": "ಇಂದಿನ ಕಾರ್ಯಗಳು:\n{}",
        "tasks_week": "ಈ ವಾರದ ಕಾರ್ಯಗಳು:\n{}",
        "overdue_tasks": "ವಿಳಂಬವಾದ ಕಾರ್ಯಗಳು:\n{}",
        "task_summary": """ಕಾರ್ಯ ಸಾರಾಂಶ:
ಒಟ್ಟು ಕಾರ್ಯಗಳು: {}
ಬಾಕಿ ಕಾರ್ಯಗಳು: {}
ಪೂರ್ಣಗೊಂಡ ಕಾರ್ಯಗಳು: {}
ವಿಳಂಬವಾದ ಕಾರ್ಯಗಳು: {}
ಇಂದಿನ ಕಾರ್ಯಗಳು: {}
ಈ ವಾರದ ಕಾರ್ಯಗಳು: {}""",
        "unknown_command": "ನಾನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲಿಲ್ಲ: {}",
        "error_processing": "ಕಾರ್ಯ ಆಜ್ಞೆಯನ್ನು ಸಂಸ್ಕರಿಸುವಲ್ಲಿ ದೋಷ: {}",
    }

    # Time-related translations
    TIME_TRANSLATIONS = {
        "today": "ಇಂದು",
        "tomorrow": "ನಾಳೆ",
        "monday": "ಸೋಮವಾರ",
        "tuesday": "ಮಂಗಳವಾರ",
        "wednesday": "ಬುಧವಾರ",
        "thursday": "ಗುರುವಾರ",
        "friday": "ಶುಕ್ರವಾರ",
        "saturday": "ಶನಿವಾರ",
        "sunday": "ಭಾನುವಾರ",
    }

    # Common task-related words
    TASK_WORDS = {
        "task": "ಕಾರ್ಯ",
        "work": "ಕೆಲಸ",
        "job": "ಕೆಲಸ",
        "assignment": "ಕಾರ್ಯ",
        "todo": "ಮಾಡಬೇಕಾದದ್ದು",
        "deadline": "ಕೊನೆಯ ದಿನ",
        "priority": "ಪ್ರಾಮುಖ್ಯತೆ",
        "urgent": "ತುರ್ತು",
        "important": "ಮುಖ್ಯ",
        "completed": "ಪೂರ್ಣಗೊಂಡ",
        "pending": "ಬಾಕಿ",
        "overdue": "ವಿಳಂಬವಾದ",
    }


class KannadaVoiceProcessor:
    """Process Kannada voice commands"""

    def __init__(self):
        self.translations = KannadaTranslations()

    def detect_language(self, command: str) -> Language:
        """Detect if the command is in Kannada or English"""
        # Check for Kannada characters (Unicode range: 0x0C80-0x0CFF)
        kannada_chars = any("\u0c80" <= char <= "\u0cff" for char in command)

        if kannada_chars:
            return Language.KANNADA
        else:
            return Language.ENGLISH

    def translate_priority_to_english(self, kannada_priority: str) -> str:
        """Translate Kannada priority to English"""
        reverse_translations = {
            v: k for k, v in self.translations.PRIORITY_TRANSLATIONS.items()
        }
        return reverse_translations.get(kannada_priority, "normal")

    def translate_priority_to_kannada(self, english_priority: str) -> str:
        """Translate English priority to Kannada"""
        return self.translations.PRIORITY_TRANSLATIONS.get(english_priority, "ಸಾಮಾನ್ಯ")

    def get_kannada_response(self, response_key: str, *args) -> str:
        """Get Kannada response message"""
        template = self.translations.RESPONSES.get(response_key, response_key)
        return template.format(*args)

    def extract_kannada_task_title(self, command: str, pattern_type: str) -> str:
        """Extract task title from Kannada command"""
        import re

        patterns = self.translations.KANNADA_COMMANDS.get(pattern_type, [])

        for pattern in patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                return match.group(1).strip()

        return ""

    def parse_kannada_deadline(self, command: str) -> tuple:
        """Parse Kannada deadline expressions"""
        import re
        from datetime import datetime, timedelta

        # Kannada time patterns
        kannada_time_patterns = [
            (r"ಇಂದು\s+(\d{1,2}:\d{2})", "today"),
            (r"ನಾಳೆ\s+(\d{1,2}:\d{2})", "tomorrow"),
            (r"(ಸೋಮವಾರ|ಮಂಗಳವಾರ|ಬುಧವಾರ|ಗುರುವಾರ|ಶುಕ್ರವಾರ|ಶನಿವಾರ|ಭಾನುವಾರ)", "day_name"),
            (r"(\d{1,2}/\d{1,2}(?:/\d{2,4})?)", "date"),
        ]

        for pattern, pattern_type in kannada_time_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                if pattern_type == "today":
                    time_part = match.group(1)
                    now = datetime.now()
                    return (
                        f"{now.strftime('%Y-%m-%d')} {time_part}",
                        command.replace(match.group(0), "").strip(),
                    )

                elif pattern_type == "tomorrow":
                    time_part = match.group(1)
                    tomorrow = datetime.now() + timedelta(days=1)
                    return (
                        f"{tomorrow.strftime('%Y-%m-%d')} {time_part}",
                        command.replace(match.group(0), "").strip(),
                    )

                elif pattern_type == "day_name":
                    day_name = match.group(1)
                    # Convert Kannada day names to English for processing
                    day_mapping = {
                        "ಸೋಮವಾರ": "monday",
                        "ಮಂಗಳವಾರ": "tuesday",
                        "ಬುಧವಾರ": "wednesday",
                        "ಗುರುವಾರ": "thursday",
                        "ಶುಕ್ರವಾರ": "friday",
                        "ಶನಿವಾರ": "saturday",
                        "ಭಾನುವಾರ": "sunday",
                    }
                    english_day = day_mapping.get(day_name.lower(), day_name)
                    return english_day, command.replace(match.group(0), "").strip()

        return None, command


# Example usage and testing
if __name__ == "__main__":
    processor = KannadaVoiceProcessor()

    # Test language detection
    test_commands = [
        "ಕಾರ್ಯ ಸೇರಿಸಿ: ಬೆಳಗ್ಗೆ ಓದು",
        "Add task: Read in the morning",
        "ಇಂದಿನ ಕಾರ್ಯಗಳು ಯಾವುವು",
        "What are my tasks today?",
    ]

    print("Testing Kannada Language Support")
    print("=" * 40)

    for command in test_commands:
        language = processor.detect_language(command)
        print(f"Command: {command}")
        print(f"Language: {language.value}")
        print()

    # Test task title extraction
    kannada_command = "ಕಾರ್ಯ ಸೇರಿಸಿ: ಬೆಳಗ್ಗೆ ಓದು"
    title = processor.extract_kannada_task_title(kannada_command, "add_task")
    print(f"Extracted task title: {title}")

    # Test response generation
    response = processor.get_kannada_response("task_added", "ಬೆಳಗ್ಗೆ ಓದು")
    print(f"Kannada response: {response}")
