"""LLM brain and local command router for Jarvis."""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.request

from .config import AIConfig, get_config
from .memory import MemoryStore
from .tools import ToolRegistry


class JarvisAI:
    def __init__(self, config: AIConfig | None = None) -> None:
        self.config = config or get_config()
        self.memory = MemoryStore(self.config.memory_db_path)
        self.tools = ToolRegistry(self.memory)

    def answer(self, user_text: str) -> str:
        text = user_text.strip()
        if not text:
            return "I did not hear a request."

        local_response = self._handle_local_command(text)
        if local_response:
            return local_response

        if self.config.provider == "ollama":
            tool_response = self._try_llm_tool_plan(text)
            if tool_response:
                return tool_response
            return self._ask_ollama(text)
        if self.config.provider == "openai":
            tool_response = self._try_llm_tool_plan(text)
            if tool_response:
                return tool_response
            return self._ask_openai(text)

        return (
            "AI mode is ready, but no LLM provider is configured. "
            "Set JARVIS_LLM_PROVIDER to ollama or openai in .env."
        )

    def _handle_local_command(self, text: str) -> str | None:
        lower = text.lower()
        remember_prefixes = (
            "remember that",
            "remember this",
            "save memory",
        )
        for prefix in remember_prefixes:
            if lower.startswith(prefix):
                memory_text = text[len(prefix) :].strip(" :,-")
                return self.tools.get("remember").run(memory_text)

        if lower.startswith("add task"):
            task_text = text[len("add task") :].strip(" :,-")
            return self.tools.get("add_task").run(task_text)

        task_match = re.match(
            r"^(?:please\s+)?(?:put|add)\s+(.+?)\s+(?:on|to|in)\s+"
            r"(?:my\s+)?(?:task list|tasks)$",
            text,
            flags=re.IGNORECASE,
        )
        if task_match:
            return self.tools.get("add_task").run(task_match.group(1))

        note_prefixes = (
            "take note",
            "add note",
            "save note",
            "note that",
            "write down",
            "make a note",
        )
        for prefix in note_prefixes:
            if lower.startswith(prefix):
                note_text = text[len(prefix) :].strip(" :,-")
                if note_text.lower().startswith("that "):
                    note_text = note_text[5:].strip()
                return self.tools.get("add_note").run(note_text)

        if any(
            command in lower
            for command in (
                "show notes",
                "read notes",
                "list notes",
                "show my notes",
                "what notes",
                "saved notes",
            )
        ):
            return self.tools.get("show_notes").run("")

        reminder_prefixes = (
            "remind me to",
            "please remind me to",
            "set a reminder to",
            "create a reminder to",
            "save a reminder to",
            "add reminder",
            "save reminder",
        )
        for prefix in reminder_prefixes:
            if lower.startswith(prefix):
                reminder_text = text[len(prefix) :].strip(" :,-")
                return self.tools.get("add_reminder").run(reminder_text)

        if any(
            command in lower
            for command in (
                "show reminders",
                "read reminders",
                "list reminders",
                "show my reminders",
                "what reminders",
                "saved reminders",
            )
        ):
            return self.tools.get("show_reminders").run("")

        task_view_commands = (
            "show tasks",
            "show my tasks",
            "list tasks",
            "list my tasks",
            "what are my tasks",
            "what tasks do i have",
            "read my tasks",
        )
        if any(command in lower for command in task_view_commands):
            return self.tools.get("show_tasks").run("")

        if lower.startswith("search memory"):
            query = text[len("search memory") :].strip(" :,-")
            return self.tools.get("search_memory").run(query)

        if "what do you remember" in lower:
            return self.tools.get("search_memory").run("")

        memory_search_match = re.match(
            r"^(?:do you remember|search your memory for|find memory about)\s+(.+)$",
            text,
            flags=re.IGNORECASE,
        )
        if memory_search_match:
            return self.tools.get("search_memory").run(memory_search_match.group(1))

        if lower in {"list tools", "what can you do"}:
            return self.tools.list_descriptions()

        if lower.startswith("open "):
            app_name = text[len("open ") :].strip(" :,-")
            return self.tools.get("open_app").run(app_name)

        return None

    def _system_prompt(self) -> str:
        memories = self.memory.recent(limit=6)
        memory_text = "\n".join(f"- {item.text}" for item in memories) or "- None yet"
        return (
            f"You are {self.config.assistant_name}, a practical personal AI assistant "
            f"for {self.config.user_name}. Be concise, useful, and honest.\n\n"
            "Known memories:\n"
            f"{memory_text}\n\n"
            "Available local tools are handled by the Python router before this prompt:\n"
            f"{self.tools.list_descriptions()}"
        )

    def _try_llm_tool_plan(self, text: str) -> str | None:
        plan = self._plan_tool_with_llm(text)
        if not plan:
            return None

        tool_name = str(plan.get("tool", "")).strip()
        argument = str(plan.get("argument", "")).strip()
        if not tool_name or tool_name == "none":
            return None

        tool = self.tools.get(tool_name)
        if not tool:
            return None

        if tool.needs_confirmation:
            return f"I need confirmation before using {tool.name}."

        return tool.run(argument)

    def _plan_tool_with_llm(self, text: str) -> dict[str, str] | None:
        system_prompt = (
            "You are a tool planner for Jarvis. Choose exactly one safe local tool "
            "only when the user is clearly asking for that action. Otherwise choose none.\n"
            "Return only JSON. Do not add markdown or explanation.\n\n"
            "Schema: {\"tool\": \"tool_name_or_none\", \"argument\": \"short argument\"}\n\n"
            "Tools:\n"
            "- remember: save a fact or preference about the user\n"
            "- search_memory: search saved memories\n"
            "- show_tasks: show saved tasks\n"
            "- add_task: add something to the task list\n"
            "- add_note: save a note or write something down\n"
            "- show_notes: show saved notes\n"
            "- add_reminder: save a reminder\n"
            "- show_reminders: show saved reminders\n"
            "- open_app: open an allowed app by name\n\n"
            "Examples:\n"
            "User: put finish report on my task list\n"
            "JSON: {\"tool\": \"add_task\", \"argument\": \"finish report\"}\n"
            "User: write down that the AI layer should stay safe\n"
            "JSON: {\"tool\": \"add_note\", \"argument\": \"the AI layer should stay safe\"}\n"
            "User: do you remember Python\n"
            "JSON: {\"tool\": \"search_memory\", \"argument\": \"Python\"}\n"
            "User: open calculator\n"
            "JSON: {\"tool\": \"open_app\", \"argument\": \"calculator\"}\n"
            "User: explain what an LLM is\n"
            "JSON: {\"tool\": \"none\", \"argument\": \"\"}"
        )
        planner_text = self._ask_model(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text},
            ],
            max_tokens=120,
        )
        return self._extract_json_object(planner_text)

    def _extract_json_object(self, text: str) -> dict[str, str] | None:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None

        try:
            data = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return None

        if not isinstance(data, dict):
            return None
        return data

    def _ask_model(
        self, messages: list[dict[str, str]], max_tokens: int | None = None
    ) -> str:
        if self.config.provider == "ollama":
            return self._ask_ollama_messages(messages, max_tokens=max_tokens)
        if self.config.provider == "openai":
            return self._ask_openai_messages(messages, max_tokens=max_tokens)
        return ""

    def _ask_ollama(self, text: str) -> str:
        return self._ask_ollama_messages(
            [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": text},
            ]
        )

    def _ask_ollama_messages(
        self, messages: list[dict[str, str]], max_tokens: int | None = None
    ) -> str:
        payload = {
            "model": self.config.ollama_model,
            "stream": False,
            "messages": messages,
        }
        if max_tokens:
            payload["options"] = {"num_predict": max_tokens}

        request = urllib.request.Request(
            f"{self.config.ollama_url}/api/chat",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                data = json.loads(response.read().decode("utf-8"))
            return data.get("message", {}).get("content", "").strip() or "No answer."
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            return f"Ollama is not available right now: {exc}"

    def _ask_openai(self, text: str) -> str:
        return self._ask_openai_messages(
            [
                {"role": "system", "content": self._system_prompt()},
                {"role": "user", "content": text},
            ]
        )

    def _ask_openai_messages(
        self, messages: list[dict[str, str]], max_tokens: int | None = None
    ) -> str:
        if not self.config.openai_api_key:
            return "OPENAI_API_KEY is missing in .env."

        try:
            from openai import OpenAI
        except ImportError:
            return "The openai package is not installed. Install it before using openai mode."

        client = OpenAI(api_key=self.config.openai_api_key)
        request_args = {
            "model": self.config.openai_model,
            "input": messages,
        }
        if max_tokens:
            request_args["max_output_tokens"] = max_tokens

        response = client.responses.create(
            **request_args,
        )
        return response.output_text.strip()
