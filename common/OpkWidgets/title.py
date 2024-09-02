import tkinter as tk

from PIL import Image, ImageTk, ImageDraw
from functools import lru_cache
from settings import *

class Title(tk.Label):
    def __init__(self, master: tk.Misc | None = None, description: str = None, **kwargs):
        super().__init__(master, compound=tk.CENTER, **kwargs)
        self._kwargs = kwargs
        self._font = kwargs.get('font', ('Futura Bk BT', 12))
        self._description = description

    @lru_cache
    def __drawText(self):
        _font = FONT(FONTLIST[self._font[0]], (self._font[1] * TkinterFontModifiyer))
        _description_font = FONT(FONTLIST['Futura Bk BT'], ((self._font[1] - 4) * TkinterFontModifiyer))
        _, _, _width, _height = _font.getbbox(self._kwargs.get('text', ''))
        _, _, desc_width, _ = _font.getbbox(self._description)

        bbox = (self.winfo_width(), self.winfo_height())
        print(bbox)
        image = Image.new('RGBA', (max(bbox[0], desc_width), bbox[1] * (1 if self._description == None else 2) - 20),
                          '#6f60')
        draw = ImageDraw.Draw(image)
        draw.text(
            (
                bbox[0] / 2 - _width / 2,
                bbox[1] / 2 - _height / 2
            ), text=self._kwargs.get('text', ''), font=_font, fill=self._kwargs.get('foreground', '#000'))
        if self._description != None:
            draw.text(
                (
                    bbox[0] / 2 - _width / 2 + 5,
                    bbox[1] / 2 + _height / 4
                ), text=self._description, font=_description_font, fill=self._kwargs.get('foreground', '#000'))

        return image

    @lru_cache
    def __render(self):
        self.update()
        self._render = ImageTk.PhotoImage(self.__drawText())
        self.configure(image=self._render, text='')

    def pack(self, **kwargs):
        '''Pack a widget in the parent widget. Use as options:
        after=widget - pack it after you have packed widget
        anchor=NSEW (or subset) - position widget according to
                                given direction
        before=widget - pack it before you will pack widget
        expand=bool - expand widget if parent size grows
        fill=NONE or X or Y or BOTH - fill widget if widget grows
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        side=TOP or BOTTOM or LEFT or RIGHT - where to add this widget.'''
        super().pack(**kwargs)
        self.__render()

    def place(self, **kwargs):
        '''Place a widget in the parent widget. Use as options:
        in=master - master relative to which the widget is placed
        in_=master - see 'in' option description
        x=amount - locate anchor of this widget at position x of master
        y=amount - locate anchor of this widget at position y of master
        relx=amount - locate anchor of this widget between 0.0 and 1.0
                    relative to width of master (1.0 is right edge)
        rely=amount - locate anchor of this widget between 0.0 and 1.0
                    relative to height of master (1.0 is bottom edge)
        anchor=NSEW (or subset) - position anchor according to given direction
        width=amount - width of this widget in pixel
        height=amount - height of this widget in pixel
        relwidth=amount - width of this widget between 0.0 and 1.0
                        relative to width of master (1.0 is the same width
                        as the master)
        relheight=amount - height of this widget between 0.0 and 1.0
                        relative to height of master (1.0 is the same
                        height as the master)
        bordermode="inside" or "outside" - whether to take border width of
                                        master widget into account'''
        super().place(**kwargs)
        self.__render()

    def grid(self, **kwargs):
        '''Position a widget in the parent widget in a grid. Use as options:
        column=number - use cell identified with given column (starting with 0)
        columnspan=number - this widget will span several columns
        in=master - use master to contain this widget
        in_=master - see 'in' option description
        ipadx=amount - add internal padding in x direction
        ipady=amount - add internal padding in y direction
        padx=amount - add padding in x direction
        pady=amount - add padding in y direction
        row=number - use cell identified with given row (starting with 0)
        rowspan=number - this widget will span several rows
        sticky=NSEW - if cell is larger on which sides will this
                    widget stick to the cell boundary'''
        super().grid(**kwargs)
        self.__render()