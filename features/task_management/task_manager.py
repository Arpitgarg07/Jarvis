"""
Voice-Controlled Task Management System for Jarvis
==================================================

This module provides a complete task management system with voice commands,
persistent storage, and integration with Jarvis's speech recognition system.

Features:
- Add tasks via voice commands
- Set deadlines and priorities
- Track completed and overdue tasks
- Daily/weekly task summaries
- Persistent JSON storage
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
from dataclasses import dataclass, asdict
from enum import Enum
from kannada_support import KannadaVoiceProcessor, Language


class Priority(Enum):
    """Task priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


@dataclass
class Task:
    """Task data structure"""
    id: str
    title: str
    description: str = ""
    priority: Priority = Priority.NORMAL
    deadline: Optional[str] = None
    created_at: str = ""
    completed: bool = False
    completed_at: Optional[str] = None
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class TaskManager:
    """Main task management class"""
    
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> None:
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [
                        Task(
                            id=task['id'],
                            title=task['title'],
                            description=task.get('description', ''),
                            priority=Priority(task.get('priority', 'normal')),
                            deadline=task.get('deadline'),
                            created_at=task.get('created_at', ''),
                            completed=task.get('completed', False),
                            completed_at=task.get('completed_at'),
                            tags=task.get('tags', [])
                        )
                        for task in data
                    ]
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []
    
    def save_tasks(self) -> None:
        """Save tasks to JSON file"""
        try:
            data = []
            for task in self.tasks:
                task_dict = {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'priority': task.priority.value,  # Convert enum to string
                    'deadline': task.deadline,
                    'created_at': task.created_at,
                    'completed': task.completed,
                    'completed_at': task.completed_at,
                    'tags': task.tags
                }
                data.append(task_dict)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def add_task(self, title: str, description: str = "", priority: Priority = Priority.NORMAL, 
                 deadline: Optional[str] = None, tags: List[str] = None) -> str:
        """Add a new task"""
        task_id = f"task_{len(self.tasks) + 1}_{int(datetime.now().timestamp())}"
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            deadline=deadline,
            tags=tags or []
        )
        self.tasks.append(task)
        self.save_tasks()
        return task_id
    
    def complete_task(self, task_id: str) -> bool:
        """Mark a task as completed"""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = True
                task.completed_at = datetime.now().isoformat()
                self.save_tasks()
                return True
        return False
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def update_task_priority(self, task_id: str, priority: Priority) -> bool:
        """Update task priority"""
        for task in self.tasks:
            if task.id == task_id:
                task.priority = priority
                self.save_tasks()
                return True
        return False
    
    def get_tasks_by_date(self, date: str = None) -> List[Task]:
        """Get tasks for a specific date or today"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        tasks = []
        for task in self.tasks:
            if task.deadline and task.deadline.startswith(date):
                tasks.append(task)
        return tasks
    
    def get_tasks_this_week(self) -> List[Task]:
        """Get all tasks for this week"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        tasks = []
        for task in self.tasks:
            if task.deadline:
                try:
                    task_date = datetime.fromisoformat(task.deadline)
                    if week_start <= task_date <= week_end:
                        tasks.append(task)
                except ValueError:
                    continue
        return tasks
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks"""
        now = datetime.now()
        overdue = []
        
        for task in self.tasks:
            if task.deadline and not task.completed:
                try:
                    deadline = datetime.fromisoformat(task.deadline)
                    if deadline < now:
                        overdue.append(task)
                except ValueError:
                    continue
        return overdue
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending (incomplete) tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_tasks_by_priority(self, priority: Priority) -> List[Task]:
        """Get tasks by priority level"""
        return [task for task in self.tasks if task.priority == priority and not task.completed]
    
    def search_tasks(self, query: str) -> List[Task]:
        """Search tasks by title or description"""
        query = query.lower()
        results = []
        for task in self.tasks:
            if (query in task.title.lower() or 
                query in task.description.lower() or
                any(query in tag.lower() for tag in task.tags)):
                results.append(task)
        return results
    
    def get_task_summary(self) -> Dict:
        """Get comprehensive task summary"""
        pending = self.get_pending_tasks()
        completed = [task for task in self.tasks if task.completed]
        overdue = self.get_overdue_tasks()
        
        priority_counts = {
            Priority.URGENT: len(self.get_tasks_by_priority(Priority.URGENT)),
            Priority.HIGH: len(self.get_tasks_by_priority(Priority.HIGH)),
            Priority.NORMAL: len(self.get_tasks_by_priority(Priority.NORMAL)),
            Priority.LOW: len(self.get_tasks_by_priority(Priority.LOW))
        }
        
        return {
            'total_tasks': len(self.tasks),
            'pending_tasks': len(pending),
            'completed_tasks': len(completed),
            'overdue_tasks': len(overdue),
            'priority_breakdown': priority_counts,
            'tasks_today': len(self.get_tasks_by_date()),
            'tasks_this_week': len(self.get_tasks_this_week())
        }


class VoiceCommandParser:
    """Parse voice commands for task management (English and Kannada)"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.kannada_processor = KannadaVoiceProcessor()
    
    def parse_command(self, command: str) -> Dict:
        """Parse voice command and return action (supports English and Kannada)"""
        command = command.lower().strip()
        
        # Detect language
        language = self.kannada_processor.detect_language(command)
        
        if language == Language.KANNADA:
            return self._parse_kannada_command(command)
        else:
            return self._parse_english_command(command)
    
    def _parse_english_command(self, command: str) -> Dict:
        """Parse English voice commands"""
        # Add task patterns
        if re.match(r'add task:?\s*(.+)', command):
            match = re.match(r'add task:?\s*(.+)', command)
            title = match.group(1).strip()
            return self._parse_add_task(title)
        
        # Add urgent task
        if re.match(r'add urgent task:?\s*(.+)', command):
            match = re.match(r'add urgent task:?\s*(.+)', command)
            title = match.group(1).strip()
            return self._parse_add_task(title, Priority.URGENT)
        
        # Mark task completed
        if re.match(r'mark task completed:?\s*(.+)', command):
            match = re.match(r'mark task completed:?\s*(.+)', command)
            task_title = match.group(1).strip()
            return {'action': 'complete_task', 'task_title': task_title}
        
        # Set priority
        if re.match(r'set task priority:?\s*(.+?)\s+to\s+(high|normal|low|urgent)', command):
            match = re.match(r'set task priority:?\s*(.+?)\s+to\s+(high|normal|low|urgent)', command)
            task_title = match.group(1).strip()
            priority = Priority(match.group(2).strip())
            return {'action': 'set_priority', 'task_title': task_title, 'priority': priority}
        
        # Show tasks
        if 'what are my tasks today' in command:
            return {'action': 'show_tasks_today'}
        
        if 'what are my tasks this week' in command:
            return {'action': 'show_tasks_week'}
        
        if 'show overdue tasks' in command:
            return {'action': 'show_overdue_tasks'}
        
        if 'task summary' in command or 'task overview' in command:
            return {'action': 'show_summary'}
        
        return {'action': 'unknown', 'command': command}
    
    def _parse_kannada_command(self, command: str) -> Dict:
        """Parse Kannada voice commands"""
        # Add task patterns
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['add_task']):
            title = self.kannada_processor.extract_kannada_task_title(command, 'add_task')
            if title:
                return self._parse_add_task(title)
        
        # Add urgent task patterns
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['add_urgent_task']):
            title = self.kannada_processor.extract_kannada_task_title(command, 'add_urgent_task')
            if title:
                return self._parse_add_task(title, Priority.URGENT)
        
        # Complete task patterns
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['complete_task']):
            title = self.kannada_processor.extract_kannada_task_title(command, 'complete_task')
            if title:
                return {'action': 'complete_task', 'task_title': title}
        
        # Set priority patterns
        priority_patterns = self.kannada_processor.translations.KANNADA_COMMANDS['set_priority']
        for pattern in priority_patterns:
            match = re.search(pattern, command, re.IGNORECASE)
            if match:
                task_title = match.group(1).strip()
                kannada_priority = match.group(2).strip()
                english_priority = self.kannada_processor.translate_priority_to_english(kannada_priority)
                priority = Priority(english_priority)
                return {'action': 'set_priority', 'task_title': task_title, 'priority': priority}
        
        # Show tasks today
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['show_tasks_today']):
            return {'action': 'show_tasks_today'}
        
        # Show tasks this week
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['show_tasks_week']):
            return {'action': 'show_tasks_week'}
        
        # Show overdue tasks
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['show_overdue']):
            return {'action': 'show_overdue_tasks'}
        
        # Task summary
        if any(re.search(pattern, command, re.IGNORECASE) for pattern in self.kannada_processor.translations.KANNADA_COMMANDS['task_summary']):
            return {'action': 'show_summary'}
        
        return {'action': 'unknown', 'command': command}
    
    def _parse_add_task(self, title: str, priority: Priority = Priority.NORMAL) -> Dict:
        """Parse add task command with deadline detection"""
        deadline = None
        description = ""
        
        # Check for deadline patterns
        deadline_patterns = [
            r'by\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+today',
            r'by\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+tomorrow',
            r'by\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            r'by\s+(\d{1,2}/\d{1,2}(?:/\d{2,4})?)',
            r'due\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+today',
            r'due\s+(\d{1,2}:\d{2}\s*(?:am|pm)?)\s+tomorrow'
        ]
        
        for pattern in deadline_patterns:
            match = re.search(pattern, title, re.IGNORECASE)
            if match:
                deadline_text = match.group(1)
                deadline = self._parse_deadline(deadline_text, title)
                title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()
                break
        
        return {
            'action': 'add_task',
            'title': title,
            'description': description,
            'priority': priority,
            'deadline': deadline
        }
    
    def _parse_deadline(self, deadline_text: str, full_text: str) -> str:
        """Parse deadline text to ISO format"""
        now = datetime.now()
        
        # Handle "today" and "tomorrow"
        if 'today' in full_text.lower():
            if ':' in deadline_text:
                time_part = deadline_text
                return f"{now.strftime('%Y-%m-%d')} {time_part}"
            return now.strftime('%Y-%m-%d')
        
        if 'tomorrow' in full_text.lower():
            tomorrow = now + timedelta(days=1)
            if ':' in deadline_text:
                time_part = deadline_text
                return f"{tomorrow.strftime('%Y-%m-%d')} {time_part}"
            return tomorrow.strftime('%Y-%m-%d')
        
        # Handle day names
        day_names = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        if deadline_text.lower() in day_names:
            days_ahead = day_names[deadline_text.lower()] - now.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            target_date = now + timedelta(days=days_ahead)
            return target_date.strftime('%Y-%m-%d')
        
        # Handle date formats
        if '/' in deadline_text:
            try:
                date_obj = datetime.strptime(deadline_text, '%m/%d')
                date_obj = date_obj.replace(year=now.year)
                if date_obj < now:
                    date_obj = date_obj.replace(year=now.year + 1)
                return date_obj.strftime('%Y-%m-%d')
            except ValueError:
                pass
        
        return deadline_text


class TaskVoiceInterface:
    """Main interface for voice-controlled task management (English and Kannada)"""
    
    def __init__(self):
        self.task_manager = TaskManager()
        self.parser = VoiceCommandParser(self.task_manager)
        self.kannada_processor = KannadaVoiceProcessor()
    
    def process_voice_command(self, command: str) -> str:
        """Process voice command and return response (supports English and Kannada)"""
        parsed = self.parser.parse_command(command)
        action = parsed.get('action')
        
        # Detect language for response
        language = self.kannada_processor.detect_language(command)
        
        if action == 'add_task':
            task_id = self.task_manager.add_task(
                title=parsed['title'],
                description=parsed.get('description', ''),
                priority=parsed.get('priority', Priority.NORMAL),
                deadline=parsed.get('deadline')
            )
            if language == Language.KANNADA:
                return self.kannada_processor.get_kannada_response('task_added', parsed['title'])
            else:
                return f"Task added: {parsed['title']}"
        
        elif action == 'complete_task':
            tasks = self.task_manager.search_tasks(parsed['task_title'])
            if tasks:
                self.task_manager.complete_task(tasks[0].id)
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('task_completed', parsed['task_title'])
                else:
                    return f"Task completed: {parsed['task_title']}"
            else:
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('task_not_found', parsed['task_title'])
                else:
                    return f"Task not found: {parsed['task_title']}"
        
        elif action == 'set_priority':
            tasks = self.task_manager.search_tasks(parsed['task_title'])
            if tasks:
                self.task_manager.update_task_priority(tasks[0].id, parsed['priority'])
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('priority_updated', parsed['task_title'])
                else:
                    return f"Priority updated for: {parsed['task_title']}"
            else:
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('task_not_found', parsed['task_title'])
                else:
                    return f"Task not found: {parsed['task_title']}"
        
        elif action == 'show_tasks_today':
            tasks = self.task_manager.get_tasks_by_date()
            if tasks:
                task_list = "\n".join([f"- {task.title}" for task in tasks])
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('tasks_today', task_list)
                else:
                    return f"Tasks for today:\n{task_list}"
            else:
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('no_tasks_today')
                else:
                    return "No tasks scheduled for today"
        
        elif action == 'show_tasks_week':
            tasks = self.task_manager.get_tasks_this_week()
            if tasks:
                task_list = "\n".join([f"- {task.title}" for task in tasks])
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('tasks_week', task_list)
                else:
                    return f"Tasks this week:\n{task_list}"
            else:
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('no_tasks_week')
                else:
                    return "No tasks scheduled this week"
        
        elif action == 'show_overdue_tasks':
            tasks = self.task_manager.get_overdue_tasks()
            if tasks:
                task_list = "\n".join([f"- {task.title}" for task in tasks])
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('overdue_tasks', task_list)
                else:
                    return f"Overdue tasks:\n{task_list}"
            else:
                if language == Language.KANNADA:
                    return self.kannada_processor.get_kannada_response('no_overdue_tasks')
                else:
                    return "No overdue tasks"
        
        elif action == 'show_summary':
            summary = self.task_manager.get_task_summary()
            if language == Language.KANNADA:
                return self.kannada_processor.get_kannada_response('task_summary', 
                    summary['total_tasks'], summary['pending_tasks'], summary['completed_tasks'],
                    summary['overdue_tasks'], summary['tasks_today'], summary['tasks_this_week'])
            else:
                return f"""Task Summary:
Total Tasks: {summary['total_tasks']}
Pending: {summary['pending_tasks']}
Completed: {summary['completed_tasks']}
Overdue: {summary['overdue_tasks']}
Tasks Today: {summary['tasks_today']}
Tasks This Week: {summary['tasks_this_week']}"""
        
        else:
            if language == Language.KANNADA:
                return self.kannada_processor.get_kannada_response('unknown_command', command)
            else:
                return f"I didn't understand: {command}"


# Example usage and testing
if __name__ == "__main__":
    # Initialize the voice interface
    voice_interface = TaskVoiceInterface()
    
    # Test commands
    test_commands = [
        "Add task: Buy groceries",
        "Add urgent task: Submit assignment by Friday",
        "Add task: Call mom by 5 PM today",
        "What are my tasks today?",
        "What are my tasks this week?",
        "Show overdue tasks",
        "Task summary"
    ]
    
    print("Testing Voice-Controlled Task Management System")
    print("=" * 50)
    
    for command in test_commands:
        print(f"\nCommand: {command}")
        response = voice_interface.process_voice_command(command)
        print(f"Response: {response}")
