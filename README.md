# Jarvis - Personal AI Voice Assistant

Jarvis is a Python-based voice assistant for Windows that can respond to commands, control your system, automate common tasks, and integrate with AI-powered features.

This project combines the original voice assistant workflow with a newer AI layer under the `jarvis_ai` package and `ai_assistant.py`, making it suitable for both local automation and experimentation with LLM-based command handling.

## Features

- Voice command assistant with speech recognition and text-to-speech
- System control such as browser actions, screenshots, volume, and window management
- Productivity tools including tasks, reminders, alarms, and focus mode
- Web and information helper functions for search, news, IP lookup, and translation
- Communication features for email and WhatsApp automation
- Entertainment features like jokes, games, and media playback
- AI-capable layer for local memory, note storage, task management, and model-driven tools
- Optional environment-based configuration for API keys and service credentials

## Tech Stack

- Python 3.11
- `pyttsx3`, `SpeechRecognition`, `pyaudio`-compatible setup
- `opencv-python-headless`
- `pyautogui`, `keyboard`, `pynput`, `psutil`
- `requests`, `beautifulsoup4`, `wikipedia`, `speedtest-cli`
- `pygame`, `gtts`, `googletrans`
- `pywhatkit`, `twilio`, `wolframalpha`
- `python-dotenv`
- SQLite-backed local memory in the AI layer

## Repository Layout

```text
.
├── ai_assistant.py              # Text-based AI interaction entry point
├── install.py                  # Dependency installer script
├── main.py                     # Main app launcher
├── Jarvismain.py               # Core assistant logic
├── requirements.txt            # Runtime dependencies
├── requirements-dev.txt        # Dev/test dependencies
├── .env.example                # Environment variable template
├── AI_UPGRADE.md               # Notes for the AI upgrade layer
├── README.md                   # Project documentation
├── core/                       # Core assistant logic and voice helpers
├── features/                   # Feature modules for search, system, entertainment, etc.
├── jarvis_ai/                  # Local AI memory/config/tooling layer
├── tests/                      # Automated tests
├── data/                       # Persistent local data files
├── assets/                     # Media and visual assets
└── LICENSE
```

## Prerequisites

- Python 3.11 recommended and required by the launcher in `main.py`
- Windows 10/11 is the primary target environment
- Microphone for voice input
- Webcam for face-recognition features
- Internet connection for web/API-based features

## Setup

1. Clone the repository:

```bash
git clone <your-repo-url>
cd "Jarvis BY arpit"
```

2. Create a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

Optional automatic package install:

```bash
python install.py
```

4. Configure environment variables:

```bash
copy .env.example .env
```

Then update `.env` with your API keys and service credentials, such as:

- `GEMINI_API_KEY`
- `GROQ_API_KEY`
- `WOLFRAM_API_KEY`
- `NEWS_API_KEY`
- `SENDER_EMAIL`
- `SENDER_PASSWORD`
- `TWILIO_SID`
- `TWILIO_TOKEN`

## Run the Assistant

Launch the main voice assistant:

```bash
python main.py
```

Run the text-based AI assistant:

```bash
python ai_assistant.py
```

## Example Commands

The assistant supports commands such as:

- "Hello"
- "What time is it?"
- "Open Google"
- "Search for Python"
- "Tell me a joke"
- "Set an alarm"
- "Remind me later"
- "Take a screenshot"
- "Translate hello to Hindi"
- "What is my IP address?"
- "Show my focus stats"

## AI Layer

The AI layer is still being expanded but includes:

- `.env`-based configuration
- SQLite memory storage
- local tool wrappers for task/note/reminder tracking
- command routing through `jarvis_ai/brain.py`
- optional model providers such as Ollama or OpenAI-like integrations

See [AI_UPGRADE.md](AI_UPGRADE.md) for more details.

## Testing

Run the test suite with:

```bash
pytest
```

Or use the project helper:

```bash
python run_tests.py
```

## Contributing

Contributions are welcome. Please keep changes focused, document new features, and validate with tests when possible.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

Thanks to these amazing people who make Jarvis better:

**GSSoC Open Source:** This project is part of GirlScript Summer of Code (GSSoC) as an open-source initiative.

**Contributors (Phase 1):** Adez017, campuscoder74, Kushanware, Jai-76, Adithyakp86, arzoo0511

<a href="https://github.com/Arpitgarg07/Jarvis/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Arpitgarg07/Jarvis" />
</a>

---

## 💬 Community & Support

- **💬 Discussions:** [GitHub Discussions](https://github.com/Arpitgarg07/Jarvis/discussions)
- **🐛 Bug Reports:** [Issues](https://github.com/Arpitgarg07/Jarvis/issues)
- **📧 Email:** [Contact Arpit](mailto:contact@arpitgarg.com)

---

## 📜 License

This project is freely available under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 🧱 Builder

Built by **Arpit Garg** ([@Arpitgarg07](https://github.com/Arpitgarg07)).

---

## 🙏 Acknowledgments

- **Tony Stark/Iron Man:** For the inspiration behind the name and vision
- **OpenCV Community:** For powerful computer vision tools
- **Python Community:** For the amazing libraries that power Jarvis
- **Contributors:** Everyone who helps improve this project
- **Users:** Thank you for choosing Jarvis

---

<div align="center">
  <img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif" width="100%">
  <p><strong>🤖 "Sometimes you gotta run before you can walk." - Tony Stark</strong></p>
  <p>Built with ❤️ and Python by Arpit Garg. Secure assistance for everyone.</p>
  <img src="https://komarev.com/ghpvc/?username=Arpitgarg07-Jarvis&label=Project%20Views&color=00BFFF&style=flat" alt="Project views" />
</div>