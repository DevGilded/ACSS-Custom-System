import tkinter as tk
import OpkCustomWidget as Otk

from settings import *

def close(master: tk.Canvas):
    global canvas, n
    if n > 0:
        canvas.destroy()
        for widget in get_all_widgets(master):
            widget.unbind('<Button-1>')
    n = 1

def get_all_widgets(widget):
    widgets = [widget]
    for child in widget.winfo_children():
        widgets.extend(get_all_widgets(child))
    return widgets

def memberInformation(master: tk.Canvas):
    canvas = tk.Canvas(master, bd=0, highlightthickness=0, 
                    #    background='red'
                       )
    canvas.place(x=2, y=50, relheight=1, height=-52, relwidth=1, width=-4)

    ageVar = tk.IntVar()

    firstName = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=20, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='First Name')
    middleInitial = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=5, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='M.I', variableLimit=2)
    lastName = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=19, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='Last Name')
    
    fbName = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=20, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='Facebook Name')
    sex = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=7, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='Sex')
    age = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=3, 
                        textVariable=ageVar, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        variableLimit=150)
    #* # bod is short for Date of Birth
    dob  = Otk.Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=12, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='MM-DD-YYYY',
                        isCalendar=True)
    
    #* First Row
    firstName.place(x=20, y=30)
    middleInitial.place(x=40+firstName._width, y=30)
    lastName.place(x=60+firstName._width+middleInitial._width, y=30)
    #* Second Row
    fbName.place(x=20, y=60+firstName._height)
    sex.place(x=40+fbName._width, y=60+firstName._height)
    age.place(x=60+fbName._width+sex._width, y=60+firstName._height)
    dob.place(x=80+fbName._width+sex._width+age._width, y=60+firstName._height)

    # phoneNum
    # IDNum

    #~ Label
    firstNameLabel = Otk.Label(canvas, 'First Name', font=FONT(FuturaHeavy, 18))
    firstNameLabel.place(y=10, x=30)
    middleInitialLabel = Otk.Label(canvas, 'Middle Initial', font=FONT(FuturaHeavy, 18))
    middleInitialLabel.place(y=10, x=25+firstName._width)
    lastNameLabel = Otk.Label(canvas, 'Last Name', font=FONT(FuturaHeavy, 18))
    lastNameLabel.place(y=10, x=70+firstName._width+middleInitial._width)

    fbNameLabel = Otk.Label(canvas, 'Facebook Name', font=FONT(FuturaHeavy, 18))
    fbNameLabel.place(y=40+firstName._height, x=30)
    sexLabel = Otk.Label(canvas, 'Sex', font=FONT(FuturaHeavy, 18))
    sexLabel.place(y=40+firstName._height, x=50+fbName._width)
    ageLabel = Otk.Label(canvas, 'Age', font=FONT(FuturaHeavy, 18))
    ageLabel.place(y=40+firstName._height, x=70+fbName._width+sex._width)
    dobLabel = Otk.Label(canvas, 'Date of Birth', font=FONT(FuturaHeavy, 18))
    dobLabel.place(y=40+firstName._height, x=90+fbName._width+sex._width+age._width)

    

def init(master: tk.Canvas):
    global canvas, n
    try:
        canvas.destroy()
    except:
        pass

    n = 0
    for widget in get_all_widgets(master):
        widget.bind('<Button-1>', lambda event: close(master))

    canvas = tk.Canvas(master, highlightthickness=2, highlightbackground=PRIMARY_COLOR, width=master.winfo_width()*0.8, height=master.winfo_height()*0.8)
    canvas.place(x=master.winfo_width()*0.1, y=master.winfo_height()*0.1)

    global close_Icon, sp, sp1
    
    close_Icon = Otk.Icon(canvas, 'assets/svg/cross-icon.svg', scale=1.5, command=lambda event: close(master))
    close_Icon.place(x=-10, relx=1, y=10, anchor='ne')

    sp = Otk.DrawLine(canvas, weight=2, orientation='vertical', width=28)
    sp.place(y=10, x=-(close_Icon._rect.size[0]+20), anchor='ne', relx=1)
    sp1 = Otk.DrawLine(canvas, weight=2, orientation='horizontal')
    sp1.place(y=45, padding=10)

    title = Otk.Label(canvas, 'Add Member', font=FONT(FuturaHeavy, 28), foreground=PRIMARY_COLOR)
    title.place(x=10, y=12)

    memberInformation(canvas)