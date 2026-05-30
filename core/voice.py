import pyttsx3
import speech_recognition as sr

_engine = pyttsx3.init('sapi5')
_voices = _engine.getProperty('voices')
_engine.setProperty('voice', _voices[0].id)
_engine.setProperty('rate', 185)


def Speak(audio: str) -> None:
    print(f"Jarvis: {audio}")
    _engine.say(audio)
    _engine.runAndWait()


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