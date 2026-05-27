"""Safe tools that the AI brain can use."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from typing import Callable

from .config import PROJECT_ROOT
from .memory import MemoryStore


ToolFunction = Callable[[str], str]


@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    run: ToolFunction
    needs_confirmation: bool = False


class ToolRegistry:
    def __init__(self, memory: MemoryStore) -> None:
        self.memory = memory
        self._tools: dict[str, Tool] = {}
        self.register_defaults()

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_descriptions(self) -> str:
        return "\n".join(
            f"- {tool.name}: {tool.description}" for tool in self._tools.values()
        )

    def register_defaults(self) -> None:
        self.register(
            Tool(
                name="remember",
                description="Save a fact, preference, or note about the user.",
                run=self._remember,
            )
        )
        self.register(
            Tool(
                name="search_memory",
                description="Search saved memories.",
                run=self._search_memory,
            )
        )
        self.register(
            Tool(
                name="show_tasks",
                description="Read the current tasks.txt file.",
                run=self._show_tasks,
            )
        )
        self.register(
            Tool(
                name="add_task",
                description="Append a task to tasks.txt.",
                run=self._add_task,
            )
        )
        self.register(
            Tool(
                name="add_note",
                description="Save a note to jarvis_notes.txt.",
                run=self._add_note,
            )
        )
        self.register(
            Tool(
                name="show_notes",
                description="Read saved notes.",
                run=self._show_notes,
            )
        )
        self.register(
            Tool(
                name="add_reminder",
                description="Save a reminder to jarvis_reminders.txt.",
                run=self._add_reminder,
            )
        )
        self.register(
            Tool(
                name="show_reminders",
                description="Read saved reminders.",
                run=self._show_reminders,
            )
        )
        self.register(
            Tool(
                name="open_app",
                description="Open an allowed Windows app by name.",
                run=self._open_app,
            )
        )

    def _remember(self, text: str) -> str:
        item = self.memory.remember(text)
        return f"Saved memory #{item.id}: {item.text}"

    def _search_memory(self, query: str) -> str:
        results = self.memory.search(query)
        if not results:
            return "I do not have a matching memory yet."
        return "\n".join(f"- {item.text}" for item in results)

    def _show_tasks(self, _: str) -> str:
        task_file = PROJECT_ROOT / "tasks.txt"
        if not task_file.exists():
            return "No tasks file exists yet."
        content = task_file.read_text(encoding="utf-8", errors="ignore").strip()
        return content or "There are no saved tasks."

    def _add_task(self, task: str) -> str:
        clean_task = task.strip()
        if not clean_task:
            return "Please give me a task to add."
        task_file = PROJECT_ROOT / "tasks.txt"
        if task_file.exists():
            existing = task_file.read_text(encoding="utf-8", errors="ignore").splitlines()
        else:
            existing = []
        next_number = len([line for line in existing if line.strip()]) + 1
        with task_file.open("a", encoding="utf-8") as file:
            file.write(f"{next_number}. {clean_task}\n")
        return f"Task added: {clean_task}"

    def _add_note(self, note: str) -> str:
        clean_note = note.strip()
        if not clean_note:
            return "Please give me a note to save."
        note_file = PROJECT_ROOT / "jarvis_notes.txt"
        with note_file.open("a", encoding="utf-8") as file:
            file.write(f"- {clean_note}\n")
        return f"Note saved: {clean_note}"

    def _show_notes(self, _: str) -> str:
        note_file = PROJECT_ROOT / "jarvis_notes.txt"
        if not note_file.exists():
            return "No notes saved yet."
        content = note_file.read_text(encoding="utf-8", errors="ignore").strip()
        return content or "No notes saved yet."

    def _add_reminder(self, reminder: str) -> str:
        clean_reminder = reminder.strip()
        if not clean_reminder:
            return "Please give me a reminder to save."
        reminder_file = PROJECT_ROOT / "jarvis_reminders.txt"
        with reminder_file.open("a", encoding="utf-8") as file:
            file.write(f"- {clean_reminder}\n")
        return f"Reminder saved: {clean_reminder}"

    def _show_reminders(self, _: str) -> str:
        reminder_file = PROJECT_ROOT / "jarvis_reminders.txt"
        if not reminder_file.exists():
            return "No reminders saved yet."
        content = reminder_file.read_text(encoding="utf-8", errors="ignore").strip()
        return content or "No reminders saved yet."

    def _open_app(self, app_name: str) -> str:
        allowed_apps = {
            "calculator": "calc.exe",
            "calc": "calc.exe",
            "notepad": "notepad.exe",
            "paint": "mspaint.exe",
            "command prompt": "cmd.exe",
            "cmd": "cmd.exe",
            "powershell": "powershell.exe",
        }
        clean_name = app_name.strip().lower()
        executable = allowed_apps.get(clean_name)
        if not executable:
            allowed = ", ".join(sorted(allowed_apps))
            return f"I can only open these apps for now: {allowed}."

        subprocess.Popen([executable])
        return f"Opening {clean_name}."
