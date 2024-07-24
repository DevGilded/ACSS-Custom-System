import tkinter as tk

import hero
import home
import sidebar

from settings import *

def on_key_press(event):
    if event.keysym == 'Escape':
        window.destroy()

if __name__ == '__main__':
    window = tk.Tk()

    WIN_POS_X = int((window.winfo_screenwidth() / 2) - WIN_POS_X)
    WIN_POS_Y = int((window.winfo_screenheight() / 2) - WIN_POS_Y)

    window.title('Association of Computer Science Students | CITE Members\' Specialization Data ')
    window.geometry(f'{WIDTH}x{HEIGHT}+{WIN_POS_X}+{WIN_POS_Y}')
    # window.attributes('-fullscreen', True)
    # window.resizable(False, False)

    canvas = tk.Canvas(window, bd=0, highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    hero.init(canvas)
    sidebar.init(canvas)
    # home.init(canvas)


    window.bind('<Key>', on_key_press)

    window.mainloop()

print('-- [ Program End ] --')