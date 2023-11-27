import CombatSystem
import EquipmentSystem
import DungeonCrawl
import Texts
import os
import time
import random
import copy
from tkinter import *

    
# Create the main window
root = Tk()
root.title("Dungeon Crawl Game")


root.iconbitmap('./pythontutorial-1.ico')

window_height = 400
window_width = 600
#get display/screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#find center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

frametop = Frame(root,padx=10,pady=10)
frametop.pack()

texttop = "Things to display and show,\nso long as they are relevant."

toptext = Label(frametop,text= texttop, fg="white", bg="black",font=(14))
toptext.pack(ipadx=10,ipady=10)

bottomframe = Frame()
bottomframe.pack(side=BOTTOM)

def startGame():
    gamerunning = True

    while gamerunning == True:
        os.system("cls")
        startbutton.pack_forget()
        DungeonCrawl.exploreDungeon()

def updateText (label,newtext):
    label.configure(text = newtext)

startbutton = Button(bottomframe, text = "Start", command = startGame)
startbutton.pack(pady=30)

# leftframe = Frame(bg="orange")
# leftframe.pack(side=LEFT)

# rightframe = Frame(bg="orange")
# rightframe.pack(side=RIGHT)

# button1 = Button(leftframe, text = "Button 1")
# button1.pack(padx = 3, pady = 3)

# button2 = Button(rightframe, text = "Button 2")
# button2.pack(padx = 3, pady = 3 )






if __name__ == "__main__":
    # Start the GUI event loop  
    root.mainloop()

    # gamerunning = True

    # while gamerunning == True:

    #     # GAME BOOTS DIRECTLY INTO DUNGEON CRAWL
    #     # HERE THE STORY AND OTHER THINGS WILL GO TOWARDS AFTER.    

    #     os.system("cls")
    #     DungeonCrawl.exploreDungeon()