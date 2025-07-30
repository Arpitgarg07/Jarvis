import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import webbrowser

def TakeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 200
        audio = r.listen(source,0,4)

    try:
        print("Understanding...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"Master said: {query}\n")

    except Exception as e:
        print("Say that again please...") 
        return "None"
    return query

query = TakeCommand().lower()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate",185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

def searchGoogle(query):

    import wikipedia as googlescrap
    Speak("According to google")

    try:
        pywhatkit.search(query)
        result = googlescrap.summary(query,1)
        Speak(result)

    except:
        Speak("No speakable output available")

def searchyoutube(query):
    if "youtube" in query:
        Speak("This is what i found on search!")
        query = query.replace("jarvis","")
        query = query.replace("youtube search","")
        query = query.replace("search on youtube","")
        web = "https://www.youtube.com/results?search_query=" + query
        webbrowser.open(web)
        Speak("Done")

    elif "youtube home page" in query:
        Speak("opening...")
        webbrowser.get('chrome').open("youtube.com")

def searchwikipedia(query):
# *Logic for executing tasks based on query
    if 'wikipedia' in query:
        Speak('Searching from Wikipedia...')
        query = query.replace("wikipedia", "")
        query = query.replace("jarvis", "")
        query = query.replace("search on wikipedia", "")
        results = wikipedia.summary(query, sentences=1)
        Speak("According to Wikipedia")
        print(results)
        Speak(results)



