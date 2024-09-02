import tkinter as tk
from typing import Literal

from common.OpkWidgets.button import Button

from functools import lru_cache

@lru_cache
def _get_global_position(widget: tk.Widget) -> tuple[int, int]:
    """return the global position of a widget bypassing its parent"""
    x, y = 0, 0
    while bool(widget.winfo_parent()):
        x += widget.winfo_x()
        y += widget.winfo_y()
        widget: tk.Widget = widget.nametowidget(widget.winfo_parent())
    return x, y

class ComboBox(Button):
    def __init__(self, master, values: dict | list,
                 background: str | None = None, foreground: str | None = None, outline: str | None = None,
                 activebackground: str | None = None, activeforeground: str | None = None, activeoutline: str | None = None,
                 hoverbackground: str | None = None, hoverforeground: str | None = None, hoveroutline: str | None = None,
                 border: int = 0, radius: int = 0, orientation: Literal['horizontal', 'vertical'] = 'horizontal', flip: bool = False,
                 corners: tuple[bool, bool, bool, bool] | None = None, side: tuple[bool, bool, bool, bool] | None = None,
                 **kwargs):
        super().__init__(master,
                         background, foreground, outline,
                         activebackground, activeforeground, activeoutline,
                         hoverbackground, hoverforeground, hoveroutline,
                         border, radius, orientation, flip, corners, side,
                         command = self.drop_value,
                         **kwargs)

        self._values = values

    def __display_list(self, widget: tk.Frame):
        children = widget.winfo_children()

        for child in children:
            if type(child) is tk.Label:
                continue
            if child.winfo_ismapped():
                child.pack_forget()
            else:
                child.pack(anchor='nw', padx=10)

    @lru_cache
    def __draw_box(self):
        self.box = tk.Canvas(highlightbackground='black', highlightthickness=1)
        self.__map_dict(self.box, self._values)

    def __map_dict(self, parent, values, isSub = False):
        for value in values:
            frame = tk.Frame(parent)
            if not isSub:
                frame.pack(anchor='nw', padx=1, pady=1)

            dropList = tk.Label(frame, text='› ' + value, font=self._font)
            dropList.pack(anchor='nw')
            for sub in values[value]:
                if type(sub) is dict:
                    self.__map_dict(frame, sub, True)
                else:
                    tk.Checkbutton(frame, text=sub, font=self._font)
            dropList.bind('<Button-1>', lambda event, widget = frame: self.__display_list(widget))

    def drop_value(self):
        if not self.box.winfo_ismapped():
            x, y = _get_global_position(self)
            y += self.winfo_height()
            self.box.place(y=y, x=x, width=self.cget('width'))
        else:
            self.box.place_forget()

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.__draw_box()

    def place(self, **kwargs):
        super().place(**kwargs)
        self.__draw_box()

    def grid(self, **kwargs):
        super().grid(**kwargs)
        self.__draw_box()