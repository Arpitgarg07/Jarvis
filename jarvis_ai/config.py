"""Configuration helpers for the Jarvis AI layer."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"


def load_env(path: Path = ENV_PATH) -> None:
    """Load simple KEY=VALUE pairs from .env without requiring extra packages."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


@dataclass(frozen=True)
class AIConfig:
    provider: str
    ollama_url: str
    ollama_model: str
    openai_api_key: str
    openai_model: str
    user_name: str
    assistant_name: str
    memory_db_path: Path


def get_config() -> AIConfig:
    load_env()
    return AIConfig(
        provider=os.getenv("JARVIS_LLM_PROVIDER", "none").strip().lower(),
        ollama_url=os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.1"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        user_name=os.getenv("JARVIS_USER_NAME", "Arpit"),
        assistant_name=os.getenv("JARVIS_ASSISTANT_NAME", "Jarvis"),
        memory_db_path=PROJECT_ROOT / "jarvis_memory.db",
    )
