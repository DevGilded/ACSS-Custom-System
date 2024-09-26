import time
import tkinter as tk

import common.Opksvg as opkSVG
import threading

import pages.extension.sidebar as sidebar
import pages.extension.hero as hero
import pages.member as member
import pages.home as home
import pages.setting as setting

from settings import *

def count_widgets(parent):
    count = 0
    
    # Function to recursively count widgets
    def traverse(widget):
        nonlocal count
        count += 1
        for child in widget.winfo_children():
            traverse(child)
    
    traverse(parent)
    return count


class Application(tk.Tk):
    SETTING = {
        'background': BLANK,
    }

    def __init__(self):
        super().__init__()
        #~ Setting window size and place the window in center position
        self.X = (self.winfo_screenwidth() // 2) - (WIDTH // 2)
        self.Y = (self.winfo_screenheight() // 2) - (HEIGHT // 2)
        self.geometry(f'{WIDTH}x{HEIGHT}+{self.X}+{self.Y}')
        self.minsize(int(WIDTH*0.93), int(HEIGHT*0.93))
        #~ Misc. Window Option
        self.configure(self.SETTING)
        # self.attributes('-fullscreen', True)
        self.title('Association of Computer Science Students | CITE Members\' Specialization Data ')

        self.event_stop = threading.Event()

        #~ PhotoImage
        self.update()
        self.Icons = tk.PhotoImage('assets/temp/image/Members-icon.png')

        #~ Frame
        self.hero = tk.Frame(self, highlightbackground='black', highlightthickness=1)
        self.sidebar = tk.Frame(self)
        self.body = tk.Frame(self)
        
        self.hero.place(relwidth=1, height=60, y=-1, x=-1, width=2)
        self.sidebar.place(relheight=1, height=-60, y=60, x=-3)
        self.body.place(relheight=1, height=-60, y=60, relwidth=1)

        self.__change_page__('member')

    def __change_page__(self, page) -> None:
        destroy_children(self.hero)
        destroy_children(self.sidebar)
        destroy_children(self.body)

        match page:
            case 'home':
                hr = hero.HOME(self.hero)
                sd = sidebar.HOME(self.sidebar, self.body)
                home.Load(self.body)
            case 'member':
                hr = hero.MEMBER(self.hero)
                sd = sidebar.MEMBER(self.sidebar, self.body)
                member.Load(self.body)
            case 'setting':
                hr = hero.SETTING(self.hero)
                sd = sidebar.SETTING(self.sidebar, self.body)
                setting.Load(self.body)
            case _:
                raise NotImplemented("Page is not Implemented")

        sd.Widgets['HomeBtn'].configure(command=lambda: self.__change_page__('home'))
        sd.Widgets['MemberBtn'].configure(command=lambda: self.__change_page__('member'))
        sd.Widgets['SettingBtn'].configure(command=lambda: self.__change_page__('setting'))


def destroy_children(parent: tk.Widget) -> None:
    if len(parent.children) > 0:
        for widget in parent.winfo_children():
            widget.destroy()

if __name__ == '__main__':
    start = time.time()

    #~ Initialize window box
    window = Application()

    # Debugging
    end = time.time()
    print(f'Time: {end - start}')
    # print(count_widgets(window))

    window.mainloop()

    # Clear all temporary svg that been turn to png
    opkSVG.clear()
