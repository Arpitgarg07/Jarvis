from fnmatch import translate
from time import sleep
from googletrans import Translator
import googletrans
from gtts import gTTS
import os
import pygame
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
        pygame.mixer.init()
        pygame.mixer.music.load("voice.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        os.remove("voice.mp3")
    except Exception:
        print("Unable to translate")
