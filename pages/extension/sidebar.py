import tkinter as tk
import common.Opktkinter as opk

from settings import *

class HOME:
    def __init__(self, master: tk.Frame, body: tk.Frame) -> None:
        self.Widgets = {
            'HomeBtn': opk.Button(master, text='Home', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'MemberBtn': opk.Button(master, text='Member', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'SettingBtn': opk.Button(master, text='Setting', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
        }

        for i, widget in enumerate(self.Widgets):
            self.Widgets[widget].place(anchor=['nw', 'w', 'sw'][i], rely=0.5*i, y=2)

        offset = max(self.Widgets['HomeBtn'].cget('width'), 
                    self.Widgets['MemberBtn'].cget('width'), 
                    self.Widgets['SettingBtn'].cget('width'))
        master.place(width=offset+1)
        body.place(width=-offset+3, x=offset-2)


class MEMBER:
    def __init__(self, master: tk.Frame, body: tk.Frame) -> None:
        self.Widgets = {
            'HomeBtn': opk.Button(master, text='Home', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'MemberBtn': opk.Button(master, text='Member', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'SettingBtn': opk.Button(master, text='Setting', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
        }

        for i, widget in enumerate(self.Widgets):
            self.Widgets[widget].place(anchor=['nw', 'w', 'sw'][i], rely=0.5*i, y=2)

        offset = max(self.Widgets['HomeBtn'].cget('width'),
                    self.Widgets['MemberBtn'].cget('width'),
                    self.Widgets['SettingBtn'].cget('width'))
        master.place(width=offset+1)
        body.place(width=-offset+3, x=offset-2)


class SETTING:
    def __init__(self, master: tk.Frame, body: tk.Frame) -> None:
        self.Widgets = {
            'HomeBtn': opk.Button(master, text='Home', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'MemberBtn': opk.Button(master, text='Member', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'SettingBtn': opk.Button(master, text='Setting', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
        }

        for i, widget in enumerate(self.Widgets):
            self.Widgets[widget].place(anchor=['nw', 'w', 'sw'][i], rely=0.5*i, y=2)

        offset = max(self.Widgets['HomeBtn'].cget('width'),
                    self.Widgets['MemberBtn'].cget('width'),
                    self.Widgets['SettingBtn'].cget('width'))
        master.place(width=offset+1)
        body.place(width=-offset+3, x=offset-2)