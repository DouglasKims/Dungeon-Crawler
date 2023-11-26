import tkinter as tk
from tkinter import ttk

# Create the main window
root = tk.Tk()
root.title("Doug's Test")

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

# Prints which key was pressed and released.
pressed_key_label = ""
def on_key_press(event):
    global pressed_key_label
    global message
    pressed_key_label = f"{event.keysym}"
    print(f"Key pressed: {event.keysym}")
    message = tk.Label(root, text=pressed_key_label)
    message.pack()


def on_key_release(event):
    global pressed_key_label
    pressed_key_label = f"{event.keysym}"
    print(f"Key released: {event.keysym}")

#prints message when button is clicked
def on_button_click():
    print("Button clicked")

# Create a button
button = ttk.Button(root, text="Click me!", command=on_button_click)

# Pack the button into the window
button.pack()

# Bind key events to functions
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)


message = tk.Label(root, text=pressed_key_label)
message.pack()

ttk.Label(root, text="Snazzy text").pack()



def select(option):
    print(option)


ttk.Button(root, text='Rock', command=lambda: select('Rock')).pack()
ttk.Button(root, text='Paper',command=lambda: select('Paper')).pack()
ttk.Button(root, text='Scissors', command=lambda: select('Scissors')).pack()

# Start the GUI event loop
root.mainloop()