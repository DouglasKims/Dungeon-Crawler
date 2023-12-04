import tkinter as tk
import Game

def setWindows():
    # Create the main window
    # root = Tk()
    # root.title("Dungeon Crawl Game")


    # root.iconbitmap('./pythontutorial-1.ico')    




    def start_game():
        entry = tk.Entry(root, width=30)
        entry.pack(pady=10)

        event_log = tk.Text(root, height=10, width= 100, state=tk.DISABLED)
        event_log.pack(side="bottom", padx= 20, pady=20)

        button = tk.Button(root, text="Update Text", command=update_text)
        button.pack(pady=10)

        start_button.forget()

        Game.startGame()

    def update_text():
        text_content = entry.get()
        event_log.config(state=tk.NORMAL)
        event_log.delete("1.0", tk.END)
    
        
        event_log.insert(tk.END, text_content + "\n")
        
        
        event_log.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

    root = tk.Tk()
    root.title("Dynamic Text Display")

    



    start_button = tk.Button(root, text="Start", command=start_game)
    start_button.pack()


    window_height = 400
    window_width = 600
    #get display/screen dimension
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    #find center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")


    root.mainloop()



    

setWindows()