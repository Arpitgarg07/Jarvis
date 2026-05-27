"""Small local memory store for Jarvis."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class MemoryItem:
    id: int
    text: str
    category: str
    created_at: str


class MemoryStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'general',
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category)"
            )

    def remember(self, text: str, category: str = "general") -> MemoryItem:
        clean_text = text.strip()
        clean_category = category.strip() or "general"
        if not clean_text:
            raise ValueError("Memory text cannot be empty.")

        created_at = datetime.now(timezone.utc).isoformat()
        with self._connect() as conn:
            cursor = conn.execute(
                "INSERT INTO memories(text, category, created_at) VALUES (?, ?, ?)",
                (clean_text, clean_category, created_at),
            )
            memory_id = int(cursor.lastrowid)
        return MemoryItem(memory_id, clean_text, clean_category, created_at)

    def recent(self, limit: int = 8) -> list[MemoryItem]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, text, category, created_at
                FROM memories
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [MemoryItem(*row) for row in rows]

    def search(self, query: str, limit: int = 8) -> list[MemoryItem]:
        clean_query = query.strip()
        if not clean_query:
            return self.recent(limit)

        pattern = f"%{clean_query}%"
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, text, category, created_at
                FROM memories
                WHERE text LIKE ? OR category LIKE ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (pattern, pattern, limit),
            ).fetchall()
        return [MemoryItem(*row) for row in rows]
