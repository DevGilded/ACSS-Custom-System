import _tkinter
import tkinter as tk
import common.Opkfilter as OpkFilter
from PIL import ImageTk, ImageDraw, Image
from tkinter import font
from typing import TypeAlias, Any, Literal, Callable
from functools import lru_cache

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

    @lru_cache
    def __draw_button(self, background: str | None = None, foreground: str | None = None, outline: str | None = None):
        self.update()

        resolution = 10

        background = background if background is not None else self._background
        foreground = foreground if foreground is not None else self._foreground
        outline = outline if outline is not None else self._outline

        _font = FONT(FONTLIST[self._font.cget('family')], (self._font.cget('size')*TkinterFontModifiyer) * resolution)
        _, _top, _width, _height = _font.getbbox(self._text)

        width = self.winfo_width() * resolution
        height = self.winfo_height() * resolution
        border = self._border * resolution
        radius = self._radius * resolution
        corners = self.corners
        # print(border)
        # print(self._kwargs.get('relief', 'sunken'))

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
            img = rect.rotate(-90 if self._is_flip else 90).crop(
                (
                    bbox[1], 
                    bbox[0], 
                    bbox[3]+1, 
                    bbox[2]+1
                ))
            return img.resize((img.size[0] // resolution, img.size[1] // resolution)) 
        img = rect.crop((bbox[0], bbox[1], bbox[2]+1, bbox[3]+1))
        return img.resize((img.size[0] // resolution, img.size[1] // resolution)) 

    @lru_cache
    def __render_button(self):
        buttonImg = self.__draw_button()
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

class Icon(tk.Label):
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

@lru_cache
def _get_global_position(widget: tk.Widget):
    '''return the gloabal position of a widget bypassing it's parent'''
    x, y = 0, 0
    while bool(widget.winfo_parent()):
        x += widget.winfo_x()
        y += widget.winfo_y()
        widget: tk.Widget = widget.nametowidget(widget.winfo_parent())
    return (x, y)

class DropDown(Button):
    def __init__(self, master, type: Literal['List', 'Toggle'], values: dict | list,
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

class Title(tk.Label):
    def __init__(self, master: tk.Misc | None = None, description: str = None, **kwargs):
        super().__init__(master, compound=tk.CENTER, **kwargs)
        self._kwargs = kwargs
        self._font = kwargs.get('font', ('Futura Bk BT', 12))
        self._description = description

    @lru_cache
    def __drawText(self):
        _font = FONT(FONTLIST[self._font[0]], (self._font[1]*TkinterFontModifiyer))
        _description_font = FONT(FONTLIST['Futura Bk BT'], ((self._font[1]-4)*TkinterFontModifiyer))
        _, _, _width, _height = _font.getbbox(self._kwargs.get('text', ''))
        _, _, desc_width, _ = _font.getbbox(self._description)

        bbox = (self.winfo_width(), self.winfo_height())
        print(bbox)
        image = Image.new('RGBA', (max(bbox[0], desc_width), bbox[1] * (1 if self._description == None else 2)-20), '#6f60')
        draw = ImageDraw.Draw(image)
        draw.text(
            (
                bbox[0]/2-_width/2, 
                bbox[1]/2-_height/2
            ), text=self._kwargs.get('text', ''), font=_font, fill=self._kwargs.get('foreground', '#000'))
        if self._description != None:
            draw.text(
                (
                    bbox[0]/2-_width/2+5, 
                    bbox[1]/2+_height/4
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

class Table(tk.Canvas):
    def __init__(self, master: tk.Misc | None = None, variables: list[str, Callable] | None = None, is_numbered: bool = True, **kwargs):
        '''Construct a canvas widget with the parent MASTER.

        Valid resource names: background, bd, bg, borderwidth, closeenough, confine, cursor, height, highlightbackground, highlightcolor, highlightthickness, insertbackground, insertborderwidth, insertofftime, insertontime, insertwidth, offset, relief, scrollregion, selectbackground, selectborderwidth, selectforeground, state, takefocus, width, xscrollcommand, xscrollincrement, yscrollcommand, yscrollincrement.'''
        try:
            self._font = kwargs.get('font', ('Futura Hv BT', 14))
            kwargs.pop('font')
        except:
            ...
        super().__init__(master, **kwargs)
        
        self._kwargs = kwargs
        self._variables: dict[str, Callable] | None = variables
        self._isNumbered = is_numbered
        self._rows: dict[int, tk.Frame] = {}
        self._columns: dict[str, tk.Label] = {}

        self.next_row = 0

        self._row_renders: dict[str, Image.Image] = {}

    def add(self, row: int, column: str, **kwargs):
        # print(f'{row = } | {column = !s}')

        if row not in self._rows:
            padding = 2

            if len(list(self._rows.items())) > 0:
                prev_row = self.value_frame.children[f'row_{row-1}_in_{column}']
                prev_row.update_idletasks()
                prev_row_height = prev_row.winfo_height() + prev_row.winfo_y() + padding
            else:
                prev_row_height = 0

            self._rows[row] = tk.Frame(self.value_frame, name=f'row_{row}_in_{column}')
            self._rows[row].place(x=0, y=prev_row_height, relwidth=1)
            self._rows[row].bind('<MouseWheel>', self.scroll_table)

            IDLabel = tk.Label(self._rows[row], text=row, font=self._font, name=f'_ID#{row}', width=5)
            IDLabel.pack(side=tk.LEFT, fill=tk.Y)
            IDLabel.update_idletasks()
            IDLabel.bind('<MouseWheel>', self.scroll_table)

        img = f'img_row_{row}_in_{column}'
        self._row_renders[img] = ImageTk.PhotoImage(self._variables[column](**kwargs))

        cell = tk.Label(self._rows[row], image=self._row_renders[img], anchor=tk.NW)
        cell.place(x=self._rows[row].children[f'_ID#{row}'].winfo_width(), 
                   relwidth=1/len(self._variables),
                   relx=(1/len(self._variables)) * list(self._variables.keys()).index(column),
                   anchor=tk.W,
                   rely=0.5)
        cell.update_idletasks()
        cell.bind('<MouseWheel>', self.scroll_table)
        self._rows[row].place(height=self.__heightest_cell(self._rows[row].children)+5)


        self.value_frame.config(height=self._rows[row].winfo_height()+self._rows[row].winfo_y()+20, width=self._rows[row].winfo_width()+self._rows[row].winfo_x())
        self.value_frame.update_idletasks()

        bbox = self.value_canvas.bbox('all')
        self.value_canvas.config(scrollregion=bbox)

        if bbox[3] > self.value_canvas.winfo_height():
            self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            self.vsb.pack_forget()

    def __heightest_cell(self, row: dict[str, tk.Widget]):
        result = []
        
        for column in row:
            result.append(row[column].winfo_height())

        return max(result)

        
    @lru_cache
    def __render(self) -> None:
        self.update()
        if self._variables == None:
            return None
            
        header_frame = tk.Frame(self, name='header')
        header_frame.place(anchor=tk.NW, relwidth=1, height=30)

        if self._isNumbered:
            temp = tk.Label(header_frame, text=' No.', font=self._font, width=5, anchor=tk.NW, background=SECONDARY_COLOR, name='number')
            temp.place(x=0, relheight=1)
            temp.update()

        temp_current_relx = 0
        for text in self._variables:
            self._columns[text] = tk.Label(header_frame, text=text, font=self._font, anchor=tk.NW,background=SECONDARY_COLOR)
            self._columns[text].place(x=header_frame.children['number'].winfo_width(), y=0, relheight=1, relwidth=1/len(self._variables), relx=temp_current_relx)
            temp_current_relx += 1/len(self._variables)

        header_frame.update()
        self.value_canvas = tk.Canvas(self, bd=0, highlightthickness=0, name='body', background='#aaa')
        self.value_canvas.place(anchor=tk.NW, y=header_frame.winfo_height()+1, relheight=1, relwidth=1, height=-header_frame.winfo_height())

        self.value_frame = tk.Frame(self.value_canvas, bd=0, highlightthickness=0, name='body', background='#aaa', width=header_frame.winfo_width())
        # self.value_frame.place(anchor=tk.NW, y=header_frame.winfo_height()+1, relheight=1, relwidth=1, height=-header_frame.winfo_height())

        self.value_canvas.create_window((0, 0), window=self.value_frame, anchor=tk.NW)

        self.vsb = tk.Scrollbar(self, orient='vertical', command=self.value_canvas.yview)
        # self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.value_canvas.configure(yscrollcommand=self.vsb.set)

        header_frame.bind('<Configure>', self.dynamic_change)
        self.value_frame.bind('<MouseWheel>', self.scroll_table)

    @lru_cache
    def scroll_table(self, event: tk.Event):
        self.value_canvas.yview_scroll(int(-1*(event.delta/120)), tk.UNITS)

    @lru_cache
    def dynamic_change(self, event: tk.Event):
        self.value_frame.config(width=event.widget.winfo_width())

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

    