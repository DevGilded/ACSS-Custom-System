import tkinter as tk

from PIL import Image, ImageTk

class Icon(tk.Label):
    def __init__(self, master: tk.Misc | None = None, image: str | None = None, **kwargs):
        super().__init__(master = master, background=master.cget('background'), **kwargs)
        self._image = Image.open(image)
        self.render = None

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.render = ImageTk.PhotoImage(self._image)
        self.configure(image=self.render)

    def place(self, **kwargs):
        super().place(**kwargs)
        self.render = ImageTk.PhotoImage(self._image)
        self.configure(image=self.render)

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self.render = ImageTk.PhotoImage(self._image)
        self.configure(image=self.render)