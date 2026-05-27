# Jarvis AI Upgrade

This branch adds the first safe foundation for a smarter Jarvis:

- `jarvis_ai/config.py` loads `.env` settings.
- `jarvis_ai/memory.py` stores local memories in SQLite.
- `jarvis_ai/tools.py` exposes safe tools like memory and tasks.
- `jarvis_ai/brain.py` routes simple commands locally and can call an LLM provider.
- `ai_assistant.py` runs a text test loop before using voice.

## Setup

1. Copy `.env.example` to `.env`.
2. Set `JARVIS_LLM_PROVIDER`.

For local Ollama:

```text
JARVIS_LLM_PROVIDER=ollama
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=gemma4:e2b
```

For OpenAI:

```text
JARVIS_LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Test Without Voice

```bash
python ai_assistant.py
```

Try:

```text
remember that I like building AI assistants in Python
what do you remember
add task finish Jarvis AI upgrade
show tasks
take note this project should use safe tools first
show notes
remind me to test the voice command tomorrow
show reminders
list tools
```

Natural wording works too. Gemma will try to map these into safe local tools:

```text
put finish the project report on my task list
write down that tool control should stay safe
what notes have I saved
save a reminder to test Jarvis tomorrow
what reminders do I have
do you remember Python automation
```

## Use From Voice Jarvis

Say one of these:

```text
AI mode
ask AI what do you remember
ask AI remember that I prefer concise answers
ask AI add task review my Jarvis project
ask AI take note the AI layer is separate from the old Jarvis loop
ask AI show notes
ask AI remind me to test Gemma voice mode
ask AI show reminders
```

The current Jarvis commands still work. This is only the first layer, so we can expand it into real tool calling step by step.

## Download The Local Model

```bash
ollama pull gemma4:e2b
```
