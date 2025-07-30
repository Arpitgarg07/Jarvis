
import pyttsx3
import speech_recognition as sr
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
rate = engine.setProperty("rate", 185)

def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, 0, 4)

    try:
        print("Understanding...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Master said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def send_call():

    # Your Twilio account SID and auth token
    account_sid = "Your_account_sid"
    auth_token = "Your_account auth_token"
    client = Client(account_sid, auth_token)


    call = client.calls.create(
        twiml=f'<Response><Say></Say></Response>',
        from_='your_twillo_number',
        to='whom_you_want_to_sent'
    )


if __name__ == '__main__':
    send_call()