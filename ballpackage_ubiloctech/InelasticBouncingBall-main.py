# Example Project using Library
# Uses library to create a simulation of bouncing balls in a room
# Creator: Sunil Baliga
# Date: 09/25/2023

from tkinter import Tk as tk
from tkinter import Canvas, Button, Frame

import random
import time
#import sys

from ballpackage_ubiloctech.Background import Background

# Save and exit function for Save and Exit Button
def saveAndExit(win: tk, background: Background):
    background.saveBackground() 
    win.destroy()

# Save and exit function for Save and Exit Button
def loadData(background: Background, rLim = 0.2, rFlag = False):
    background.loadBackground(rLim, rFlag)
   

# Main function
if __name__ == "__main__":

    random.seed()
    #initialization
    w_part = 100
    t_delay = 0.1
    rLim = 0.1
    rFlag = True
    saveThread = None
    threadFlag = True
    #Main window and canvas objects
    window = tk()
    w_width = window.winfo_screenwidth()*0.7
    w_height = window.winfo_screenheight()*0.7
    f_height = window.winfo_screenheight() * 0.1
    f_width = window.winfo_screenwidth()*0.5

    window.minsize(int(window.winfo_screenwidth()*0.9), int(window.winfo_screenheight()*0.9))
    window.title("Bouncing Ball Demo - Conservation of Momentum and Energy")
   
    canvas = Canvas(window, width = w_width, height = w_height, bg="black")

    # Define Canvas Background object
    background = Background(w_width, w_height, w_part, w_part, window, canvas, 20, t_delay,'blue',10,1)

    buttonFrame = Frame(window)
    buttonFrame.pack(side='top')
    # Load button
    loadButton = Button(buttonFrame, text = "Load",command=lambda:loadData(background, rLim, rFlag))
    # Save and Exit button
    saveExitButton = Button(buttonFrame, text = "Save & Exit", command=lambda:saveAndExit(window, background))
    #Exit button and associated binding
    exitButton = Button(buttonFrame, text = "Exit",command = window.destroy)

    #Pack and layout GUI
    canvas.pack()
    loadButton.pack(side='left')
    saveExitButton.pack(side='left')
    exitButton.pack(side='right')

   
    canvas.update()

    window.after_idle(background.multiBallBounce, rLim, rFlag, saveThread, threadFlag)
    prev_time = time.time()
    
    window.mainloop()

    
    
    

   
        
    

   




