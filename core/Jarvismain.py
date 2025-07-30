 
#? install all library use in this by cd "pip install _______"
import pyttsx3 
import speech_recognition as sr 
import datetime
import webbrowser
import cv2
import os
import requests
import random
import time
import sys
import pyautogui
import speedtest
import requests
import numpy
import subprocess
from os import startfile
from bs4 import BeautifulSoup
from plyer import notification
from nltk.chat.util import Chat, reflections
from requests import get
from pygame import mixer
from pywikihow import RandomHowTo, search_wikihow
from Whatsapp import sendMessage
from battery import check_battery
import pygame
#! If you want to use password then comment out
  
# # Paste this just below your import files
# for i in range(3):
#     a = input("Enter Password to open Jarvis :- ")
#     pw_file = open("password.txt","r")
#     pw = pw_file.read()
#     pw_file.close()
#     if (a==pw):
#         print("WELCOME SIR ! PLZ SPEAK [WAKE UP] TO LOAD ME UP")
        
#         break
#     elif (i==2 and a!=pw):
#         exit()

#     elif (a!=pw):
#         print("Try Again")


#& Initialize the text-to-speech engine using the 'sapi5' speech API.
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')   # Available voice in you system.
engine.setProperty('voice', voices[0].id)   # Set the voice property to the first voice in the list.
rate = engine.setProperty("rate",185)   # Set the speech rate to 185. Higher values will increase the speech rate.

#* Function to speak the provided audio using pyttsx3 text-to-speech engine.
def Speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Initialize a boolean variable 'is_paused' and set it to False
is_paused = False

#^ For taking all commands and listen the user voices.
def TakeCommand():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1       # Set the pause threshold to 1 second.
        # r.energy_threshold = 200
        audio = r.listen(source,0,4)        # Listen to the audio from the microphone, with optional timeout of 4 seconds.

    try:
        print("Understanding...")    
        query = r.recognize_google(audio, language='en-in')     #* Recognize the speech using Google's speech recognition API.
        print(f"Master said: {query}\n")

    except Exception as e:
        print("Say that again please...") 
        return "None"
    return query        # Return the recognized speech as the output of the function.


#? Dictionary to store contact information with names as keys and phone numbers as values.
contact_dict = {
    "Name": "PHONE_NUMBER",
    # Add more contacts as needed.
}

#// To run alarm.py we use this.
def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

#// For exit Greeting.
goodbyes = ['You are great!', 'Thanks for using me!', 'Nice meeting with you!']
pygame.init()
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("coin.mp3")



#############################################################################################################^

save_path = "Lock Screen photos\\lock."

recognizer = cv2.face.LBPHFaceRecognizer_create() # Local Binary Patterns Histograms
recognizer.read('trainer\\trainer.yml')   #load trained model
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath) #initializing haar cascade for object detection approach

font = cv2.FONT_HERSHEY_SIMPLEX #denotes the font type


id = 2 #number of persons you want to Recognize


names = ['','arpit','raja']  #names, leave first empty bcz counter starts from 0


cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) #cv2.CAP_DSHOW to remove warning
cam.set(3, 640) # set video FrameWidht
cam.set(4, 480) # set video FrameHeight

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

# flag = True

while True:

    ret, img =cam.read() #read the frames using the above created object

    converted_image = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)  #The function converts an input image from one color space to another

    faces = faceCascade.detectMultiScale( 
        converted_image,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(minW), int(minH)),
       )
    

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2) #used to draw a rectangle on any image

        id, accuracy = recognizer.predict(converted_image[y:y+h,x:x+w]) #to predict on every single image

        # Check if accuracy is less them 100 ==> "0" is perfect match 
        if (accuracy < 100):
            id = names[id]
            accuracy = "  {0}%".format(round(100 - accuracy))
            print("Verification Succesful!")


        else:
            id = "unknown"
            accuracy = "  {0}%".format(round(100 - accuracy))
            print("Please try again...")
            

        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
        cv2.putText(img, str(accuracy), (x+5,y+h-5), font, 1, (255,255,0), 1)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
            
    if id == "unknown":
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        save_path = r"Lock Screen photos"
        filename = "screenshot.png"
        screenshot.save(os.path.join(save_path, filename))
        print(f"Screenshot saved as {os.path.join(save_path, filename)}")
        print("Exiting system due to unknown identity.")
        Speak("Exiting system due to unknown identity.")
        print("try again")
        exit()

    elif id == "arpit" or id == "name2":
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        save_path = r"Lock Screen photos"
        filename = "screenshot.png"
        screenshot.save(os.path.join(save_path, filename))
        print(f"Screenshot saved as {os.path.join(save_path, filename)}")
        break         # Press 'ESC' for exiting video

    if len(faces) == 0:
        time.sleep(1)
        screenshot = pyautogui.screenshot()
        save_path = r"Lock Screen photos"
        filename = "screenshot.png"
        screenshot.save(os.path.join(save_path, filename))
        print(f"Screenshot saved as {os.path.join(save_path, filename)}")        
        print("Your Face is not detected, Please come in bright area.")
        Speak("Your Face is not detected, Please come in bright area.")
        exit()

        
# Do a bit of cleanup
print("Face Recognization Succesfull")
Speak("Face Recognization Succesfull")
cam.release()
cv2.destroyAllWindows()


########################################################################################################^

subprocess.Popen(["python", "intro.py"], shell=True)
time.sleep(17) #!HERE YOU TYPE SECONDS THAT HAVE BEEN TAKEN TO COMPLETE GIF
pyautogui.hotkey('Alt','f4')

if __name__ == "__main__": 
#! For Executing all tasks.
    while True:
        query = TakeCommand().lower()

        #* To Wake up Jarvis.
        if "wake up" in query or "start" in query or "makeup" in query or "breakup"in query:
            from GreetMe import greetMe
            greetMe()
            #* We will use again while True to pause and play jarvis.
            while True:
                query= TakeCommand().lower()

                # Set the path to the Chrome executable
                # Which browser you want to use to execute you can use here.
                chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
                # Configure the web browser to use.
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
    

                #* To Pause the jarvis we will use it.
                if "go to sleep" in query:
                    Speak("Ok sir, you can call me anytime.")
                    break

                elif "translate" in query:
                    from Translator import translategl
                    query = query.replace("jarvis translate","")
                    query = query.replace("translate","")
                    translategl(query)

                elif "joke" in query:
                    from joke import jokes
                    jokes()
 
                #####################################################!
                elif "change password" in query:
                    Speak("What's the new password")
                    new_pw = input("Enter the new password\n")
                    new_password = open("password.txt","w")
                    new_password.write(new_pw)
                    new_password.close()
                    Speak("Done sir")
                    Speak(f"Your new password is{new_pw}")
                ######################################################!

                #^ Normal Conversation.
                elif "hello" in query or "yo" in query or "hey there" in query or "hey" in query or "hi " in query or "hi" in query or "hello arvis" in query or "hi arpit" in query or "hlo" in query or "ram ram" in query or "good morning" in query:
                    Speak("Hello sir, How are you!")
                elif "i am fine" in query:
                    Speak("Great! What about yourself?")
                elif "how are you" in query or "how r you" in query or "how r u" in query:
                    Speak("Perfect sir!")
                elif 'namaste' in query or "ram ram" in query:
                    Speak("ram ram, Master!")
                elif "kaise ho" in query or "tum ho kaise" in query:
                    Speak("I am good, thanks for asking!")
                elif "Flip a coin" in query or "coin flip" in query or "toss a coin" in query or "toss" in query:
                    outcome = random.choice(["head", "tail"])
                    # Speak(random.choice(["head", "tail"]))

                    if outcome == "head":
                        coin_sound.play()
                    else:
                        coin_sound.play()
                    print(f"The coin landed on {outcome}!")
                    Speak(f"The coin landed on {outcome}!")
                elif "thanks" in query or "thank" in query or "thank you" in query or "thanks bro" in query:
                    Speak("My pleasure.")
                elif "you are great" in query:
                    Speak("Thank You!, for your compliment.")
                elif "Gm" in query or "good morning" in query or "morning" in query or "subhprabhat" in query:
                    Speak("Good Morning Sir!")
                elif "good evening" in query or "evening" in query:
                    Speak("Good Evening Sir!")
                elif "Good afternoon" in query or "noon" in query or "good afternoon" in query:
                    Speak("Good Afternoon Sir!")
                elif "feeling sleepy" in query or "good night" in query:
                    Speak("Ok sir, if you want to close then speak [exit]")
                elif "hate" in query:
                    Speak("I'm sorry you have been hurt.")
                elif "you are lying" in query or "lie" in query:
                    Speak("Please correct me if i am wrong!, if you can't do then go and correct yourself")
                elif "tumhe kisne banaya" in query or "who made you" in query:
                    Speak("The Great Mater Arpit Garg had made me!")
                elif "fine" in query:
                    Speak("Great!, How may I assist?")
                elif "good" in query:
                    Speak("Thanks!. It's always nice talking with people who care about their health :) ")

                #! By this Function be can know our battery percentage.
                elif "battery" in query:
                    from battery import battery
                    battery()

                #! To Remember jarvis anything.
                elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    Speak("You told me to"+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()
                elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    Speak("You told me to" + remember.read())  

                #*Focus Mode Function.
                elif "focus mode" in query:
                    a = int(input("Are you sure that you want to enter focus mode :- [1 for YES / 2 for NO "))
                    if (a==1):
                        Speak("Entering the focus mode....")
                        os.startfile("FocusMode.py")
                        exit()
                    else:
                        pass
     
                elif "show my focus" in query:
                    from FocusGraph import focus_graph
                    focus_graph()

                elif "open game" in query:
                    from game import game_play
                    game_play()                

                #^ Playing playlist from youtube.
                elif 'play playlist' in query:
                    url = "https://www.youtube.com/watch?v=DbiRVNeZPnw&list=PLpmsNGoQrkhF1nNjDVXAcyVsNnLOdw_1h&pp=gAQBiAQB8AUB"
                    Speak("Music playing...")
                    webbrowser.get('chrome').open(url)
                    print("Music playing...")

                elif 'our channel' in query:
                    url = "https://www.youtube.com/channel/UCAi-EONczHNaAqr_Ff3HRsA"
                    Speak("Channel opening...")
                    webbrowser.get('chrome').open(url)
                    print("Channel opening...")

                elif 'youtube audio library' in query:
                    url = "https://studio.youtube.com/channel/UCAi-EONczHNaAqr_Ff3HRsA/music"
                    Speak("opening audio library...")
                    webbrowser.get('chrome').open(url)
                    print("opening audio library...")

                #& Finding you current location.
                elif 'my location' in query or 'where i am' in query:
                    from Location import My_Location
                    My_Location()

                #^ To reaching any website or page.
                elif "google" in query:
                    import wikipedia as googlescrap
                    query = query.replace("jarvis","")
                    query = query.replace("google search","")
                    query = query.replace("google","")
                    from SearchNow import searchGoogle
                    searchGoogle(query)

                elif "youtube" in query:
                    from SearchNow import searchyoutube
                    searchyoutube(query)
                
                elif "wikipedia" in query:
                    from SearchNow import searchwikipedia
                    searchwikipedia(query)

                #& Youtube Running Shortcuts.
                elif "full screen mode" in query:
                    pyautogui.press("f")
                    print("video played in full screen")
                elif "theater mode" in query:
                    pyautogui.press("t")
                    print("video played in theater mode")
                elif "mini player mod" in query:
                    pyautogui.press("i")
                    print("video played in miniplayer mode")
                elif "pause" in query:
                    pyautogui.press("k")
                    Speak("video paused")
                elif "play" in query:
                    pyautogui.press("k")
                    Speak("video played")
                elif "rewind" in query:
                    pyautogui.press("j")
                    print("video rewind")
                elif "forward" in query:
                    pyautogui.press("l")
                    print("video forwarded")
                elif "previous video" in query:
                    pyautogui.press("Shift","p")
                    Speak("Switching...")
                elif "next video" in query:
                    pyautogui.press("Shift","n")
                    Speak("Switching...")
                elif "mute" in query:
                    pyautogui.press("m")
                    Speak("video muted")
                elif "volume increse" in query:
                    from keyboard import volumeup
                    Speak("Turning volume up,sir")
                    volumeup()
                elif "volume down" in query:
                    from keyboard import volumedown
                    Speak("Turning volume down, sir")
                    volumedown()

                #^ open direct Websites.
                elif 'speed test by chrome' in query:
                    webbrowser.get('chrome').open("fast.com")         
        
                elif 'stackoverflow' in query:
                    webbrowser.get('chrome').open("stackoverflow.com")  
        
                elif 'amazon' in query:
                    webbrowser.get('chrome').open("amazon.in")
        
                elif'flipkart' in query:
                    webbrowser.get('chrome').open("flipkart.com")
        
                elif 'meesho' in query or 'open me show' in query:
                    webbrowser.get('chrome').open("meesho.com")
        
                elif'myntra' in query:
                    webbrowser.get('chrome').open("myntra.com")

                #* Windows shortcut
                elif "minimise" in query or "minimize" in query:
                    from Dictapp import minimize_window
                    minimize_window()

                elif "stick screen" in query or "unpin screen" in query or "pin screen" in query:
                    from Dictapp import pin_screen
                    pin_screen()

                elif "switch tab" in query or "switch app" in query:
                    from Dictapp import switchtab
                    switchtab()

                elif "screenshot" in query:
                    from Dictapp import take_screenshot
                    take_screenshot()

                elif "click photo" in query or "click my photo" in query:
                    from Dictapp import click_photo
                    click_photo()

                elif "open search" in query:
                    from Dictapp import open_search
                    open_search()
            
                elif "close window" in query or "close tab" in query:
                    from Dictapp import close_window
                    close_window()

                elif "close my computer" in query:
                    from Dictapp import lock_pc
                    lock_pc()

                elif "home" in query or "close all" in query:
                    from Dictapp import go_to_home_screen
                    go_to_home_screen()
            
                elif "reload" in query:
                    from Dictapp import reload_page
                    reload_page()
            
                elif "maximize" in query or "maximise" in query:
                    from Dictapp import maximize_window
                    maximize_window()
        
                elif "brightness" in query or "screen light" in query:
                    Speak("at which level")
                    from Dictapp import adjust_brightness
                    adjust_brightness()    
                
                #! Opening any app and any Software.
                elif "open" in query:   #EASY METHOD
                    query = query.replace("open","")
                    query = query.replace("jarvis","")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(1)
                    Speak("Launching Sir...")
                    pyautogui.press("enter")   

                #! Closing any app and Software.
                elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

                #& To listen newses.
                elif "news" in query:
                    from NewsRead import latestnews
                    latestnews()

                #^ Send whatsapp message by pyautogui
                elif "whatsapp message" in query:
                    from Whatsappmessage import sendwhatsapp
                    sendwhatsapp()

                #* Send any message by command
                elif "whatsapp" in query:
                    from Whatsapp import sendMessage
                    sendMessage(contact_dict)

                #~ Direct internet speed.
                elif "internet speed" in query:
                    wifi  = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    Speak(f"Wifi download speed is {download_net}")
                    Speak(f"Wifi Upload speed is {upload_net}")
                
                #! Send Call by Twilio.
                elif "send call" in query:
                    from sendcall import send_call
                    send_call()


                #* To Speak Current time.
                elif 'time' in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                    print(f"Sir, the time is {strTime}") 
                    Speak(f"Sir, the time is {strTime}") 

                #& For set an alarm.
                elif "set an alarm" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")    
                    print(f"Sir, the time is {strTime}") 
                    print("input time example:- 10 and 10 and 10")
                    Speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    Speak("Done, alarm set.")

                #*Reminder set.
                elif "remind me" in query:
                    from reminder import remindme
                    remindme()

                #^ Web ip address finding
                elif "ip ad dress" in query:
                    ip = get('https://api.ipify.org').text
                    print(f"your IP address is {ip}")
                    Speak(f"your IP address is {ip}")

                #^ To know the current temperature of city.
                elif "temperature" in query:
                    search = "temperature in rajasthan"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    Speak(f"current{search} is {temp}")

                #* To Calculate any digit.
                elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)
     
                #! For exit from Jarvis.
                elif 'exit' in query:
                    Speak(random.choice(goodbyes))
                    sys.exit()

                elif "shutdown the system" in query:
                    Speak("Are You sure you want to shutdown")
                    print("Do you wish to shutdown your PC? (yes/no)")
                    shutdown = TakeCommand().lower()
                    if shutdown == "yes":
                        Speak("Ok, Sir system is going to shutdown.")
                        os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                        Speak("OK, Sir!")
                        break

                elif "logout" in query:
                    Speak('logging out in 5 second')
                    time.sleep(5)
                    os.system("shutdown - l")
                
                elif "schedule my day" in query:
                    tasks = [] #Empty list 
                    Speak("Do you want to clear old tasks (Plz speak YES or NO)")
                    query = TakeCommand().lower()
                    if "yes" in query:
                        file = open("tasks.txt","w")
                        file.write(f"")
                        file.close()
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        i = 0
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()
                    elif "no" in query:
                        i = 0
                        no_tasks = int(input("Enter the no. of tasks :- "))
                        for i in range(no_tasks):
                            tasks.append(input("Enter the task :- "))
                            file = open("tasks.txt","a")
                            file.write(f"{i}. {tasks[i]}\n")
                            file.close()

                elif "show my schedule" in query:
                    file = open("tasks.txt","r")
                    content = file.read()
                    file.close()
                    mixer.init()
                    mixer.music.load("notification.mp3")
                    mixer.music.play()
                    notification.notify(
                        title = "My schedule :-",
                        messageschedule = content,
                        timeout = 15
                        )
                
                
                #* send email Function.
                if "write an email" in query:
                    print("To whom do you want to send the email?")
                    Speak("To whom do you want to send the email?")
      
                    recipient_name = TakeCommand().lower()
                    from sendemail import recipient_mapping
                    recipient_email = recipient_mapping.get(recipient_name)
          
                    if recipient_email:
                        print("What's the subject of the email?")
                        Speak("What's the subject of the email?")
                        subject = TakeCommand().lower()
                        from sendemail import send_email
                        from sendemail import sender_email
                        from sendemail import sender_password
          
                        print("What's the content of the email?")
                        Speak("What's the content of the email?")
                        content = TakeCommand().lower()
          
                      
                        send_email(sender_email, sender_password, recipient_email, subject, content)
                    else:
                        print("Sorry, the recipient's email address is not found.")
                        Speak("Sorry, the recipient's email address is not found.")      



                


