from fnmatch import translate
from time import sleep
from googletrans import Translator
import googletrans
from gtts import gTTS
import os
from playsound import playsound
import time

from core.voice import Speak, TakeCommand

def translategl(query):
    Speak("SURE SIR")
    print(googletrans.LANGUAGES)
    translator = Translator()
    Speak("Choose the language in which you want to translate")
    b = input("To_Lang :- ")
    text_to_translate = translator.translate(query, src="auto", dest=b)
    text = text_to_translate.text
    try:
        speakgl = gTTS(text=text, lang=b, slow=False)
        speakgl.save("voice.mp3")
        playsound("VOICE.mp3")
        time.sleep(5)
        os.remove("voice.mp3")
    except Exception:
        print("Unable to translate")
