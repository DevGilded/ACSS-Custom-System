import tkinter as tk
import OpkCustomWidget as Otk

import addMember

from settings import *

header = {
    'No.': 80,
    'Personal Information': 500,
    'Specialization': 350,
    'Standing': 0
}

def standing(canvas: tk.Canvas, level: int = 0, score: int = 0):
    rect = tk.Canvas(canvas, bd=0, highlightthickness=0)
    rect.place(x=header['No.']+header['Personal Information']+header['Specialization'], y=0, height=119)

    levelLabel = Otk.Label(rect, 'Year Lever', font=FONT(FuturaHeavy, 18), foreground='#000')
    Mlevel = Otk.Label(rect, level if level > 0 else 'N/A', font=FONT(FuturaBook, 16), foreground='#000')
    scoreLabel = Otk.Label(rect, 'Admission Score (Freshman)', font=FONT(FuturaHeavy, 18), foreground='#000')
    Mscore = Otk.Label(rect, score if score > 0 else 'N/A', font=FONT(FuturaBook, 16), foreground='#000')
    
    levelLabel.place(x=0, y=20, anchor='w')
    Mlevel.place(x=10, y=42, anchor='w')
    scoreLabel.place(x=0, y=70, anchor='w')
    Mscore.place(x=10, y=92, anchor='w')

def specialization(canvas: tk.Canvas):
    rect = tk.Canvas(canvas, bd=0, highlightthickness=0)
    rect.place(x=header['No.']+header['Personal Information'], y=0, height=119, width=header['Specialization'])

def memberInfo(canvas: tk.Canvas, name: str = 'N/A', fbAccount: str = 'N/A', sex: str = 'Male', age: int = 1, birthDate: str = '01-12-2000', phoneNum: str = 'N/A', IDNum: str = 'N/A'):
    rect = tk.Canvas(canvas, bd=0, highlightthickness=0)
    rect.place(x=header['No.'], y=0, height=119, width=header['Personal Information'])

    nameLabel = Otk.Label(rect, 'Name', font=FONT(FuturaHeavy, 18), foreground='#000')
    Mname = Otk.Label(rect, name, font=FONT(FuturaBook, 16), foreground='#000')
    facebookLabel = Otk.Label(rect, 'Facebook Account', font=FONT(FuturaHeavy, 18), foreground='#000')
    Mfacebook = Otk.Label(rect, fbAccount, font=FONT(FuturaBook, 16), foreground='#000')

    Msex = Otk.Label(rect, f'Sex: {sex}', font=FONT(FuturaBook, 16), foreground='#000')
    Mage = Otk.Label(rect, f'Age: {age}', font=FONT(FuturaBook, 16), foreground='#000')
    MbirthDate = Otk.Label(rect, f'Date of Birth: {birthDate}', font=FONT(FuturaBook, 16), foreground='#000')
    MphoneNum = Otk.Label(rect, f'Phone No: {phoneNum}', font=FONT(FuturaBook, 16), foreground='#000')
    MIDNum = Otk.Label(rect, f'ID No: {IDNum}', font=FONT(FuturaBook, 16), foreground='#000')
    
    nameLabel.place(x=0, y=20, anchor='w')
    Mname.place(x=0, y=42, anchor='w')
    facebookLabel.place(x=0, y=70, anchor='w')
    Mfacebook.place(x=0, y=92, anchor='w')

    Msex.place(x=300, y=20, anchor='w')
    Mage.place(x=300, y=20*2, anchor='w')
    MbirthDate.place(x=300, y=20*3, anchor='w')
    MphoneNum.place(x=300, y=20*4, anchor='w')
    MIDNum.place(x=300, y=20*5, anchor='w')

def No(canvas, num):
    rect = tk.Canvas(canvas, bd=0, highlightthickness=0)
    rect.place(x=0, y=0, height=119, width=header['No.'])
    Number = Otk.Label(rect, num+1, font=FONT(FuturaBook, 18), foreground='#000')
    Number.place(x=15, rely=0.5, anchor='w')

def init(master: tk.Canvas):
    global canvas
    try:
        canvas.destroy()
    except:
        pass

    global p1, category, deleteBtn, editBtn, sp, importIcon, addIcon, printIcon, tbl

    canvas = tk.Canvas(master, bd = 0, highlightthickness=0)
    canvas.place(y=59, x=79, 
                 width=-79, height=-59,
                 relwidth=1, 
                 relheight=1)
    
    p1 = Otk.Label(canvas, 'Filter by', font=FONT(FuturaHeavy, 16), foreground='#000')
    p1.place(x=25, y=20)
    category = Otk.Button(canvas, '-- Choose a Category --', font=FONT(FuturaBook, 16), foreground='#fff', background=PRIMARY_COLOR, radius=5, padding=10)
    category._canHover = False
    category.place(x=100, y=8)

    deleteBtn = Otk.Button(canvas, 'Delete', font=FONT(FuturaBook, 16), width=100, background=ERROR_COLOR, padding=10)
    deleteBtn.place(relx=1, anchor='ne', x=-10, y=8)
    editBtn = Otk.Button(canvas, 'Edit', font=FONT(FuturaBook, 16), width=100, background=SUCCES_COLOR, padding=10)
    editBtn.place(relx=1, anchor='ne', x=-140, y=8)

    sp = Otk.DrawLine(canvas, weight=2, orientation='vertical', width=42)
    sp.place(y=5, relx=1, x=-280)

    importIcon = Otk.Icon(canvas, 'assets/svg/export-as-excel-icon.svg', scale=1.5)
    importIcon.place(relx=1, anchor='ne', x=-300, y=13)
    addIcon = Otk.Icon(canvas, 'assets/svg/add-entry-icon.svg', scale=1.5, name='Add Member', command=lambda event: addMember.init(master))
    addIcon.place(relx=1, anchor='ne', x=-340, y=13)
    printIcon = Otk.Icon(canvas, 'assets/svg/print-icon.svg', scale=1.5)
    printIcon.place(relx=1, anchor='ne', x=-385, y=13)
    
    # sp1 = Otk.DrawLine(canvas, weight=2)
    # sp1.place(y=50, padding=10)

    tbl = Otk.Table(canvas, header, font=FONT(FuturaHeavy, 16), padding=(10, 5), height=600)
    for i in range(3):
        temp_row = tbl.create_row(height=120)
        temp_row['canvas']
        No(temp_row['canvas'], i)
        memberInfo(temp_row['canvas'])
        specialization(temp_row['canvas'])
        standing(temp_row['canvas'])
    tbl.place(y=50)