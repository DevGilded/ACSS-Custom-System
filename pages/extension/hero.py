import tkinter as tk
import common.Opktkinter as opk
import common.Opksvg as opkSVG

from settings import *

class MEMBER:
    def __init__(self, master: tk.Frame) -> None:
        icon = opkSVG.ToPNG('assets/svg/Members-icon.svg', 1.5)

        self.Widgets = {
            'TitleLbl': opk.Title(master, text='CITE Members\' Specialization Data', description='Association of Computer Science Students',font=('Futura Hv BT', 18)),
            'PageIcon': opk.Icon(master, image=icon, compound=tk.CENTER),
            'SearchEntry': tk.Entry(master, font=('Futura Bk BT', 18), width=25),
            'IDBtn': opk.Button(master, text='ID', font=('Futura Bk BT', 14), width=10, radius=20, background=PRIMARY_COLOR, foreground=BLANK, activeforeground=BLANK),
            'NameBtn': opk.Button(master, text='Name', font=('Futura Bk BT', 14), width=10, radius=20, background=PRIMARY_COLOR, foreground=BLANK, activeforeground=BLANK),
            'SearchLbl': tk.Label(master, text='Search by', font=('Futura Bk BT', 12)),
        }
        
        self.Widgets['TitleLbl'].place(anchor='w', rely=0.5, x=-3)
        self.Widgets['TitleLbl'].update()
        for widget in self.Widgets:
            if not self.Widgets[widget].winfo_ismapped():
                self.Widgets[widget].pack(anchor='e', side='right', padx=2 if widget != 'PageIcon' else 10)