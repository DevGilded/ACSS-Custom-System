import time
import tkinter as tk
import common.Opksvg as opkSVG

import pages.extension.sidebar as sidebar
import pages.extension.hero as hero
import pages.member as member

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

        #~ Hero
        hero.MEMBER(self.hero)

        #~ Sidebar
        sidebar.MEMBER(self.sidebar, self.body)

        #~ Body
        member.Instance(self.body)


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
