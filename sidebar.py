import tkinter as tk
import OpkCustomWidget as Otk

import member
import home

from settings import *

def separator(canvas: tk.Canvas):
    padding = 5
    height = 85
    width = 10
    canvas.create_line(padding, height, canvas.winfo_width()-padding, height, fill='#FFD700', width=width)
    canvas.create_line(padding, height+width, canvas.winfo_width()-padding, height+width, fill=PRIMARY_COLOR, width=width)


def init(master: tk.Canvas):
    canvas = tk.Canvas(master, highlightbackground='gray65', highlightthickness=1)
    canvas.place(y=60-2, x=-1, 
                 width=80, 
                 relheight=1)
    
    global header, homeBtn, memberBtn, settingBtn

    # header = Otk.Label(canvas, text='ACSS CITE', font=FONT(Lobster, 64), foreground=PRIMARY_COLOR)
    # header.place(y=10)

    homeBtn = Otk.Button(canvas, text='HOME', font=FONT(FuturaHeavy, 24), foreground='white', 
                         outline=PRIMARY_COLOR, width=180, border=1, radius=100, angle=-90, background=PRIMARY_COLOR,
                         corners=[True, True, False, False],
                         command=lambda event: home.init(master))
    homeBtn.place(y=10, x=0)
    memberBtn = Otk.Button(canvas, text='MEMBERS', font=FONT(FuturaHeavy, 24), foreground='white', 
                         outline=PRIMARY_COLOR, width=180, border=1, radius=100, angle=-90, background=PRIMARY_COLOR,
                         corners=[True, True, False, False],
                           command=lambda event: member.init(master))
    memberBtn.place(y=230, x=0)
    settingBtn = Otk.Button(canvas, text='SETTINGS', font=FONT(FuturaHeavy, 24), foreground='white', 
                         outline=PRIMARY_COLOR, width=180, border=1, radius=100, angle=-90, background=PRIMARY_COLOR,
                         corners=[True, True, False, False],
                           command=lambda event: master.delete('all'))
    settingBtn.place(y=450, x=0)

    return 0