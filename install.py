import subprocess
import sys

# Dictionary containing all Jarvis runtime dependencies mapped to None (latest version)
# You can pin specific versions if needed (e.g., {"numpy": "1.26.4"})
jarvis_dependencies = {
    "pyttsx3": None,  # Text-to-speech engine
    "SpeechRecognition": None,  # Speech recognition utility
    "opencv-python-headless": None,  # Computer vision (headless)
    "requests": None,  # HTTP requests
    "numpy": None,  # Array/Math computations
    "pyautogui": None,  # GUI automation
    "speedtest-cli": None,  # Internet speed testing
    "beautifulsoup4": None,  # Web scraping
    "plyer": None,  # Platform notifications/hardware APIs
    "nltk": None,  # Natural Language Toolkit
    "pygame": None,  # Audio/game framework
    "pyjokes": None,  # Generate jokes
    "googletrans": None,  # Google Translate API wrapper
    "gtts": None,  # Google Text-to-Speech
    "pywhatkit": None,  # WhatsApp/YouTube automation
    "wikipedia": None,  # Wikipedia summary fetcher
    "twilio": None,  # SMS/Call API
    "pywikihow": None,  # WikiHow article scraper
    "playsound": None,  # Play audio files
    "pillow": None,  # Image processing
    "python-dotenv": None,  # Environment variables configuration
    "win10toast": None,  # Windows 10 toast notifications
    "psutil": None,  # Process and system utilities
    "wolframalpha": None,  # WolframAlpha computational engine
    "wmi": None,  # Windows Management Instrumentation
    "pynput": None,  # Control and monitor input devices
    "pywin32": None,  # Windows extensions for Python
    "keyboard": None,  # Global keyboard tracking/control
    "matplotlib": None,  # Plotting/Data visualization
}


def install_jarvis_libraries(library_dict: dict):
    """Installs all packages specified in the dictionary sequentially."""
    total = len(library_dict)
    print(f"Beginning installation of {total} Jarvis dependencies...\n")

    for index, (package, version) in enumerate(library_dict.items(), start=1):
        package_spec = f"{package}=={version}" if version else package
        print(f"[{index}/{total}] Installing {package_spec}...")

        try:
            # Use sys.executable to target the active Python environment safely
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_spec]
            )
            print(f"-> Successfully installed {package}\n")
        except subprocess.CalledProcessError as e:
            print(f"-> Error installing {package}: {e}\n")


if __name__ == "__main__":
    install_jarvis_libraries(jarvis_dependencies)
