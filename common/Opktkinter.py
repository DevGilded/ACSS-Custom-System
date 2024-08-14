import _tkinter
import tkinter as tk
import common.Opkfilter as OpkFilter
from PIL import ImageTk, ImageDraw, Image, ImageFont
from tkinter import font
from typing import TypeAlias, Any, Literal

from settings import *

_FontDescription: TypeAlias = (
    str  # "Helvetica 12"
    | font.Font  # A font object constructed in Python
    | list[Any]  # ["Helvetica", 12, BOLD]
    | tuple[str]  # ("Liberation Sans",) needs wrapping in tuple/list to handle spaces
    | tuple[str, int]  # ("Liberation Sans", 12)
    | tuple[str, int, str]  # ("Liberation Sans", 12, "bold")
    | tuple[str, int, list[str] | tuple[str, ...]]  # e.g. bold and italic
    | _tkinter.Tcl_Obj  # A font object constructed in Tcl
)

class Button(tk.Button):
    def __init__(self, master,
                 background: str | None = None, foreground: str | None = None, outline: str | None = None, 
                 activebackground: str | None = None, activeforeground: str | None = None, activeoutline: str | None = None, 
                 hoverbackground: str | None = None, hoverforeground: str | None = None, hoveroutline: str | None = None, 
                 border: int = 0, radius: int = 0, orientation: Literal['horizontal', 'vertical'] = 'horizontal', flip: bool = False,
                 corners: tuple[bool, bool, bool, bool] | None = None, side: tuple[bool, bool, bool, bool] | None = None,
                 **kwargs):
        super().__init__(master = master, compound = tk.CENTER, 
                         background = master.cget('background'), 
                         activebackground = master.cget('background'),
                         foreground=foreground, activeforeground=activeforeground,
                         border=0, highlightthickness = 0, cursor='hand2',
                         **kwargs)
        
        self._text = kwargs.get('text', '')
        self._font = kwargs.get('font', ('Arial', 18))
        self._font = font.Font(family=self._font[0], size=self._font[1])
        
        self._background: str = background if background is not None else '#0000'
        self._foreground: str = foreground if foreground is not None else '#000'
        self._outline: str = outline if outline is not None else '#000'
        self._activebackground: str = activebackground if activebackground is not None else '#000'
        self._activeforeground: str = activeforeground if activeforeground is not None else '#000'
        self._activeoutline: str = activeoutline if activeoutline is not None else '#000'
        self._hoverbackground: str = hoverbackground if hoverbackground is not None else self._background
        self._hoverforeground: str = hoverforeground if hoverforeground is not None else self._foreground
        self._hoveroutline: str = hoveroutline if hoveroutline is not None else self._outline

        self._resolution = 5
        self._radius = radius
        self._border = border
        self.corners = corners
        self.side = side
        if self.side is not None:
            if not any(self.side):
                raise ValueError(f'Must have one side')
        self._orientation = orientation
        self._is_flip = flip

        self._kwargs = kwargs

    def __draw_button(self, background: str | None = None, foreground: str | None = None, outline: str | None = None):
        self.update()
        background = background if background is not None else self._background
        foreground = foreground if foreground is not None else self._foreground
        outline = outline if outline is not None else self._outline

        _font = FONT(FuturaHeavy, (self._font.cget('size')*1.318))
        _, _top, _width, _height = _font.getbbox(self._text)

        width = self.winfo_width()
        height = self.winfo_height()
        border = self._border
        radius = self._radius
        corners = self.corners
        # print(border)
        print(self._kwargs.get('relief', 'sunken'))

        rect_size = max(width, height) * 2

        rect = Image.new('RGBA', (rect_size, rect_size), '#0f00')

        bbox = (rect_size // 2 - width // 2,
                rect_size // 2 - height // 2,
                (rect_size // 2 - width // 2) + width-1, 
                (rect_size // 2 - height // 2) + height-1)

        #~ Draw Button and text
        draw = ImageDraw.Draw(rect)
        draw.rounded_rectangle(
            bbox,
            width = border,
            radius = radius,
            corners=corners,
            fill = background,
            outline = outline
        )
        if self.side is not None:
            sideBbox = (0,0,0,0)
            if not self.side[0]:
                ...
            elif not self.side[1]:
                ...
            elif not self.side[2]:
                ...
            elif not self.side[3]:
                sideBbox = (bbox[0]+border, bbox[3]-border, bbox[2]-border, bbox[3])
            draw.rectangle(sideBbox, fill='#0000')
        if self._orientation == 'vertical':
            draw.text(
                (bbox[0] + width // 2 - _width // 2, bbox[1] + height // 2 - _height // 2 - (_top // 2 if not OpkFilter.have_tail(self._text) else 0) - 1),
                text = self._text,
                font = _font,
                fill = foreground,
            )

        #~ Result
        if self._orientation == 'vertical':
            return rect.rotate(-90 if self._is_flip else 90).crop(
                (
                    bbox[1], 
                    bbox[0], 
                    bbox[3]+1, 
                    bbox[2]+1
                ))
        return rect.crop((bbox[0], bbox[1], bbox[2]+1, bbox[3]+1))

    def __render_button(self):
        buttonImg = self.__draw_button()
        # buttonImg.save(f'{self._text}.png')
        self.render = ImageTk.PhotoImage(buttonImg)
        self.configure(image=self.render, 
                       width=buttonImg.width+(3 if self._kwargs.get('relief', 'sunken') == 'sunken' else 1), 
                       height=buttonImg.height+(3 if self._kwargs.get('relief', 'sunken') == 'sunken' else 1))
        if self._orientation == 'vertical':
            self.configure(text='')

    def __binding(self):
        self.bind('<Enter>', self.__hover)
        self.bind('<Leave>', self.__hover)

    def __hover(self, event: tk.Event):
        # print(type(event.type))
        if event.type == tk.EventType.Enter:
            self.__draw_button()
        elif event.type == tk.EventType.Leave:
            self.__draw_button()
        self.__render_button()

    def pack(self, **kwargs):
        super().pack(**kwargs)
        self.__render_button()

    def place(self, **kwargs):
        super().place(**kwargs)
        self.__render_button()

class Label(tk.Label):
    def __init__(self, master: tk.Misc | None = None, image: str | None = None, **kwargs):
        super().__init__(master = master, **kwargs)
        self._image = Image.open(image)

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