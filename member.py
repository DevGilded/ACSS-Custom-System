import tkinter as tk

def init(master: tk.Canvas):
    global canvas
    try:
        canvas.destroy()
    except:
        pass

    print(list(master.children))
    canvas = tk.Canvas(master, bd = 0, highlightthickness=0)
    canvas.place(y=0, x=300, 
                 relwidth=1, 
                 relheight=1)
    

