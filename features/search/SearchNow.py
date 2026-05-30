import webbrowser
import wikipedia
import pywhatkit
from core.voice import Speak


def searchGoogle(query: str) -> None:
    Speak("Searching Google...")
    try:
        pywhatkit.search(query)
        result = wikipedia.summary(query, sentences=1)
        Speak(result)
    except Exception:
        Speak("No results found.")


def searchyoutube(query: str) -> None:
    query = (query
             .replace("jarvis", "")
             .replace("youtube search", "")
             .replace("search on youtube", "")
             .strip())
    Speak("Opening YouTube.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")


def searchwikipedia(query: str) -> None:
    query = (query
             .replace("wikipedia", "")
             .replace("jarvis", "")
             .strip())
    Speak("Searching Wikipedia...")
    try:
        result = wikipedia.summary(query, sentences=2)
        Speak(result)
    except Exception:
        Speak("Could not find results on Wikipedia.")