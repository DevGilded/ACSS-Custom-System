import tkinter as tk

from settings import *

class Load:
    def __init__(self, master: tk.Frame) -> None:

        self.Widgets: dict[str, tk.Widget] = {
            'Coming_Soon': tk.Label(master, text='Coming Soon!', font=('Futura Bk BT', 32))
        }

        self.Widgets['Coming_Soon'].place(rely=0.5, relx=0.5, anchor=tk.CENTER)

