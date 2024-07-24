import tkinter as tk
import OpkCustomWidget as Otk

from settings import *

def init(master: tk.Canvas):
    canvas = tk.Canvas(master, highlightbackground='gray65', highlightthickness=1)
    canvas.place(y=-1, x=0, 
                 relwidth=1, 
                 height=60)
    
    global title, p, p1, memberIcon

    title = Otk.Label(canvas, 'CITE Members\' Specializtion Data', font=FONT(FuturaHeavy, 24), foreground='#000')
    title.place(y=10, x=5)
    p = Otk.Label(canvas, 'Association of Computer Science Students', font=FONT(FuturaBook, 18), foreground='#000')
    p.place(y=33,x=8)
    p1 = Otk.Label(canvas, 'Search by', font=FONT(FuturaBook, 16), foreground='#000')
    p1.place(rely=0.5, y=-p1._height/2,x=-500,relx=1)

    memberIcon = Otk.Icon(canvas, 'assets/svg/Members-icon.svg')
    memberIcon.place(relx=1, x=-memberIcon._rect.size[0]-10, y=memberIcon._rect.size[1])
    


    return 0