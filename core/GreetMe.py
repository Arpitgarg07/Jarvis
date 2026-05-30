import datetime
from core.voice import Speak

# *Greet when it started.
def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour<=12:
        Speak("Good Morning, Sir.")
    elif hour >= 12 and hour<=18:
        Speak("Good Afternoon, Sir.")   
    else:
        Speak("Good Evening, Master arpit.")

    Speak("I am Jarvis. How can I help you?")  





