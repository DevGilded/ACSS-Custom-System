import tkinter as tk
from settings import *
import common.Opktkinter as opk
import common.Opksvg as opkSVG

class Application(tk.Tk):
    SETTING = {
        'background': BLANK,
    }

    def __init__(self):
        super().__init__()
        #~ Setting window size and place the window in center position
        X = (self.winfo_screenwidth() // 2) - (WIDTH // 2)
        Y = (self.winfo_screenheight() // 2) - (HEIGHT // 2)
        self.geometry(f'{WIDTH}x{HEIGHT}+{X}+{Y}')
        self.minsize(int(WIDTH*0.93), int(HEIGHT*0.93))
        #~ Misc. Window Option
        self.configure(self.SETTING)
        self.title('Association of Computer Science Students | CITE Members\' Specialization Data ')

        #~ PhotoImage
        # self.Icons = {}
        # for icon in Icons:
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
        self.HeroWidget = {
            'TitleLbl': tk.Label(self.hero, text='CITE Members\' Specialization Data', font=('Futura Hv BT', 18)),
            'DescLbl': tk.Label(self.hero, text='Association of Computer Science Students', font=('Futura Bk BT', 16)),
            'PageIcon': opk.Label(self.hero, image=Icons['Member'], compound=tk.CENTER),
            'SearchEntry': tk.Entry(self.hero, font=('Futura Bk BT', 18), width=25),
            'IDBtn': opk.Button(self.hero, text='ID', font=('Futura Bk BT', 14), width=10, radius=20, background=PRIMARY_COLOR, foreground=BLANK),
            'NameBtn': opk.Button(self.hero, text='Name', font=('Futura Bk BT', 14), width=10, radius=20, background=PRIMARY_COLOR, foreground=BLANK),
            'SearchLbl': tk.Label(self.hero, text='Search by', font=('Futura Bk BT', 12)),
        }
        
        index = 0
        self.HeroWidget['TitleLbl'].place(anchor='nw')
        self.HeroWidget['TitleLbl'].update()
        self.HeroWidget['DescLbl'].place(anchor='nw', y=self.HeroWidget['TitleLbl'].winfo_height()-8)
        self.HeroWidget['DescLbl'].lower()
        self.HeroWidget['DescLbl'].update()
        for widget in self.HeroWidget:
            if self.HeroWidget[widget].winfo_ismapped():
                continue
            self.HeroWidget[widget].pack(anchor='e', side='right', padx=2 if widget != 'PageIcon' else 10)


        #~ Sidebar
        self.SidebarWidget = {
            'HomeBtn': opk.Button(self.sidebar, text='Home', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'MemberBtn': opk.Button(self.sidebar, text='Member', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
            'SettingBtn': opk.Button(self.sidebar, text='Setting', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False)),
        }

        index = 0
        for widget in self.SidebarWidget:
            self.SidebarWidget[widget].place(anchor=['nw', 'w', 'sw'][index], rely=0.5*index, y=2)
            index += 1
        offset = max(self.SidebarWidget['HomeBtn'].cget('width'), 
                                     self.SidebarWidget['MemberBtn'].cget('width'), 
                                     self.SidebarWidget['SettingBtn'].cget('width'))
        self.sidebar.place(width=offset+1)
        self.body.place(width=-offset+3, x=offset-2)


if __name__ == '__main__':
    Icons = {
        'Member': opkSVG.ToPNG('assets/svg/Members-icon.svg', 1.5),
    }

    #~ Intialize window box
    try:
        window = Application()
        window.mainloop()
    except Exception as e:
        print(f'An error occurred: {e}')
    opkSVG.clear()