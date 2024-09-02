import tkinter as tk
import common.Opktkinter as opk
import common.Opksvg as opkSVG

from settings import *

class Load:
    def __init__(self, master: tk.Frame) -> None:

        self.Widgets: dict[str, tk.Widget] = {
            'Coming_Soon': tk.Label(master, text='Coming Soon!')
        }

        self.Widgets['Coming_Soon'].place(rely=0.5, relx=0.5)

