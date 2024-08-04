import tkinter as tk

def init(master: tk.Canvas):
    global canvas
    try:
        canvas.destroy()
    except:
        pass

    print(list(master.children))
    canvas = tk.Canvas(master, bd = 0, highlightthickness=0, background='blue')
    canvas.place(y=59, x=79, 
                 relwidth=1, 
                 relheight=1)

    