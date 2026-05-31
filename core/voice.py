import speech_recognition as sr
import win32com.client as wincl
import keyboard


def Speak(audio: str) -> None:
    print(f"Jarvis: {audio}")
    speaker = wincl.Dispatch("SAPI.SpVoice")
    speaker.Speak(audio)


def TakeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Press ESC to skip)")
        r.adjust_for_ambient_noise(source, duration=0.3)
        r.pause_threshold = 0.8
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return "None"
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception:
        print("Say that again please...")
        return "None"
    
# def TakeCommand() -> str:
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         r.adjust_for_ambient_noise(source, duration=0.5)  # ← ye add karo
#         r.pause_threshold = 0.8
#         r.energy_threshold = 300  # ← ye add karo
#         audio = r.listen(source, timeout=0, phrase_time_limit=5)
#     try:
#         print("Understanding...")
#         query = r.recognize_google(audio, language='en-in')
#         print(f"You said: {query}\n")
#         return query
#     except Exception:
#         print("Say that again please...")
#         return "None"