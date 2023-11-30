# import tkinter as tk
# from tkinter import ttk

# # Create the main window
# root = tk.Tk()
# root.title("Doug's Test")

# root.iconbitmap('./pythontutorial-1.ico')

# window_height = 400
# window_width = 600
# #get display/screen dimension
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()

# #find center point
# center_x = int(screen_width/2 - window_width / 2)
# center_y = int(screen_height/2 - window_height / 2)

# root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

# # Prints which key was pressed and released.
# pressed_key_label = ""
# def on_key_press(event):
#     global pressed_key_label
#     global message
#     pressed_key_label = f"{event.keysym}"
#     print(f"Key pressed: {event.keysym}")
#     message = tk.Label(root, text=pressed_key_label)
#     message.pack()


# def on_key_release(event):
#     global pressed_key_label
#     pressed_key_label = f"{event.keysym}"
#     print(f"Key released: {event.keysym}")

# #prints message when button is clicked
# def on_button_click():
#     print("Button clicked")

# # Create a button
# button = ttk.Button(root, text="Click me!", command=on_button_click)

# # Pack the button into the window
# button.pack()

# # Bind key events to functions
# root.bind("<KeyPress>", on_key_press)
# root.bind("<KeyRelease>", on_key_release)


# message = tk.Label(root, text=pressed_key_label)
# message.pack()

# ttk.Label(root, text="Snazzy text").pack()



# def select(option):
#     print(option)


# ttk.Button(root, text='Rock', command=lambda: select('Rock')).pack()
# ttk.Button(root, text='Paper',command=lambda: select('Paper')).pack()
# ttk.Button(root, text='Scissors', command=lambda: select('Scissors')).pack()

# # Start the GUI event loop
# root.mainloop()

BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"  # Reset to default color

# Bright versions
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colors (add 10 to the color code)
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

# MATH TEST
import math

a = 1/3

b = a*5

print (f"{BLUE}This text is blue, {CYAN} this text is cyan, {GREEN} this text is green.")
print (f"{MAGENTA}This text is blue, {RED} this text is cyan, {YELLOW} this text is green.")
print (f"{BLUE}This text is blue, {CYAN} this text is cyan, {BRIGHT_GREEN} this text is green.")
print (f"{BRIGHT_BLUE}This text is blue, {BG_RED} this text is cyan, {BG_YELLOW}{RED} this text is green.{RESET}")
print (f"{BRIGHT_YELLOW}This text is blue, {BG_BLACK}{WHITE} this text is cyan, {BG_WHITE}{BLACK} this text is green.")

print(b)
if b < 2:
    print("b is less than 2")


    # e_tec = 5
    # a_tec = ["A",3]
    # b_tec = ["B",5]
    # c_tec = ["C",7]
    # party=[a_tec,b_tec,c_tec]

    # spelldamage = 20
    # print(spelldamage)

    # for n in party:
    #     spelldamage = abs(round( spelldamage * ((math.sqrt(n[1])/10-1)) ))
    #     print (f"{spelldamage} for {n[0]}")

    # attack = 90 * abs((math.sqrt(5)/100)-(math.sqrt(10)/100)+1)

    # print (attack)