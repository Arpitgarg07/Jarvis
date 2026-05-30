import speech_recognition as sr
import win32com.client as wincl


def Speak(audio: str) -> None:
    print(f"Jarvis: {audio}")
    speaker = wincl.Dispatch("SAPI.SpVoice")
    speaker.Speak(audio)


def TakeCommand() -> str:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=0, phrase_time_limit=4)
    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query
    except Exception:
        print("Say that again please...")
        return "None"