import tkinter as tk
import OpkCustomWidget as Otk

from settings import *

def init(master: tk.Canvas):
    canvas = tk.Canvas(master, highlightbackground='gray65', highlightthickness=1)
    canvas.place(y=-1, x=0, 
                 relwidth=1, 
                 height=60)
    
    global title, p, p1, searchID, searchName, memberIcon, memberSearch

    title = Otk.Label(canvas, 'CITE Members\' Specialization Data', font=FONT(FuturaHeavy, 24), foreground='#000')
    title.place(y=10, x=5)
    p = Otk.Label(canvas, 'Association of Computer Science Students', font=FONT(FuturaBook, 18), foreground='#000')
    p.place(y=33,x=8)

    canvas.update()   
    print(canvas.winfo_width(), canvas.winfo_height())

    memberIcon = Otk.Icon(canvas, 'assets/svg/Members-icon.svg', scale=1.3, name='Member')
    memberIcon.place(relx=1, rely=0.5, anchor='e', x=-20)
    memberSearch = Otk.Entry(canvas, outline=PRIMARY_COLOR, foreground=PRIMARY_COLOR, border=1, displayText='Search', font=FONT(FuturaBook, 16),width=25)
    memberSearch.place(relx=1, rely=0.5, anchor='e', x=-70)
    searchID = Otk.Button(canvas, 'ID Number', font=FONT(FuturaBook, 16), foreground='#fff', background=PRIMARY_COLOR, width=80, padding=10)
    searchID.place(relx=1, rely=0.5, anchor='e', x=-420)
    searchName = Otk.Button(canvas, 'Name', font=FONT(FuturaBook, 16), foreground='#fff', background=PRIMARY_COLOR, width=80, padding=10)
    searchName.place(relx=1, rely=0.5, anchor='e', x=-530)
    p1 = Otk.Label(canvas, 'Search by', font=FONT(FuturaBook, 16), foreground='#000')
    p1.place(relx=1, rely=0.5, anchor='e', x=-640)

    return 0