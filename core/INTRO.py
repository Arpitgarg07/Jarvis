from tkinter import *
from PIL import Image, ImageTk, ImageSequence
import time
import pygame
from pygame import mixer
import pyautogui

mixer.init()

root = Tk()
root.geometry("1100x600")

def play_gif():
    root.lift()
    root.attributes("-topmost", True)
    img = Image.open("jarvis.gif")
    lbl = Label(root)
    lbl.place(x=0, y=0)
    i = 0
    mixer.music.load("jarvis.mp3")
    mixer.music.play()
    
    for img in ImageSequence.Iterator(img):
        img = img.resize((1100, 600))
        img = ImageTk.PhotoImage(img)
        lbl.config(image=img)
        root.update()
        time.sleep(0.05)
    
    root.quit()
      # Exit gracefully without using root.destroy()

play_gif()
root.mainloop()

