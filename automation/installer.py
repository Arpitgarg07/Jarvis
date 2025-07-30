import subprocess

libraries = [
    'pyttsx3',
    'SpeechRecognition',
    'datetime',
    'webbrowser',
    'opencv-python-headless',
    'requests',
    'random2',
    'pyautogui',
    'speedtest-cli',
    'numpy',
    'beautifulsoup4',
    'plyer',
    'nltk',
    'pygame',
    'win10toast',
    'psutil',
    'wolframalpha',
    'wmi',
    'time',
    'ctypes',
    'sys',
    'tkinter',
    'PIL',
    'pygame',
    'pyjokes',
    'pynput',
    'cv2',
    'googletrans',
    'gtts',
    'pywhatkit',
    'wikipedia',
    'twilio',
    'smtplib',
    'fnmatch',
    'playsound', 
    'mouse',
]

for library in libraries:
    subprocess.call(['pip', 'install', library])

print("Libraries installed successfully.")
