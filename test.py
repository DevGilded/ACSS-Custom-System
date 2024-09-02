import tkinter as tk
import tkinter.ttk as ttk
import common.Opksvg as opkSVG
import common.Opktkinter as opk

import pages.member as member
import pages.extension.hero as hero
import common.Opkfilter as OpkFilter
import pages.extension.sidebar as sidebar

from settings import *
from tkinter import font
from PIL import Image, ImageTk, ImageDraw
from common.OpkImage import image_text, combine_two_image
from typing import Literal

def personal_info(**kwargs):
    name: str = kwargs.get('name', 'N/A')
    facebookAccount: str = kwargs.get('facebookAccount', 'N/A')
    sex: str = kwargs.get('sex', 'N/A')
    age: str = kwargs.get('age', '17+')
    birth: str = kwargs.get('birth', 'N/A')
    phoneNum: str = kwargs.get('phoneNum', 'N/A')
    schoolID: str = kwargs.get('schoolID', 'N/A')
    yearLevel: str = kwargs.get('yearLevel', 'N/A')
    admissionScore: str = kwargs.get('admissionScore', 'N/A')

    resolution = 4

    default_font = FONT(FuturaBook, (14*TkinterFontModifiyer) * resolution)
    heavy_font = FONT(FuturaHeavy, (14*TkinterFontModifiyer) * resolution)

    main_img = Image.new('RGBA', (0, 0), '#FFF0')

    columns = {
        1: [image_text('Name ', heavy_font),
            image_text(name, default_font),
            image_text(' ', default_font),
            image_text('Facebook Account ', heavy_font),
            image_text(facebookAccount, default_font)],
            
        2: [image_text(f'Sex: {sex}', default_font),
            image_text(f'Age: {age}', default_font),
            image_text(f'Date of Birth: {birth}', default_font),
            image_text(f'Phone Number: {phoneNum}', default_font),
            image_text(f'ID: {schoolID}', default_font)],
            
        3: [image_text('Year Level', heavy_font),
            image_text(yearLevel, default_font),
            image_text(' ', default_font),
            image_text('Admission Score [Freshman]', heavy_font),
            image_text(admissionScore, default_font)]
    }

    for column in columns:
        column_img = Image.new('RGBA', (0, 0), '#fff0')

        for img in columns[column]:
            column_img = combine_two_image(column_img, img)

        main_img = combine_two_image(main_img, column_img, orientation='horizontal')

    return main_img.resize((round(main_img.size[0] / resolution), round(main_img.size[1] / resolution)))

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
        X = (self.winfo_screenwidth() // 2) - (WIDTH // 2)
        Y = (self.winfo_screenheight() // 2) - (HEIGHT // 2)
        self.geometry(f'{WIDTH}x{HEIGHT}+{X}+{Y}')
        self.minsize(int(WIDTH*0.93), int(HEIGHT*0.93))
        #~ Misc. Window Option
        self.configure(self.SETTING)
        # self.attributes('-fullscreen', True)
        self.title('Test Area')

        # self.table = Table(self, {'Column 1': personal_info, 'Column 2': personal_info})
        # self.table.place(x=0, y=0, relwidth=0.9, relx=0.05, relheight=0.8, rely=0.1)

        # for i in range(20):
        #     self.table.add(i+1, 'Column 1')
        #     self.table.add(i+1, 'Column 2')
        
        HomeBtn = Button(self, text='Home', font=('Futura Hv BT', 20), orientation='vertical', flip=True, background=PRIMARY_COLOR, foreground=BLANK, width=13, radius=48, corners=(True, True, False, False))
        HomeBtn.place(x=0, y=0)

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

        resolution = 6

        background = background if background is not None else self._background
        foreground = foreground if foreground is not None else self._foreground
        outline = outline if outline is not None else self._outline

        _font = FONT(FONTLIST[self._font.cget('family')], (self._font.cget('size')*TkinterFontModifiyer) * resolution)
        _, _top, _width, _height = _font.getbbox(self._text)

        width = self.winfo_width() * resolution
        height = self.winfo_height() * resolution
        border = self._border * resolution
        radius = self._radius * resolution
        corners = self.corners * resolution
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


class Table(tk.Canvas):
    def __init__(self, master: tk.Misc | None = None, variables: list[str, callable] | None = None, isNumbered: bool = True, **kwargs):
        '''Construct a canvas widget with the parent MASTER.

        Valid resource names: background, bd, bg, borderwidth, closeenough, confine, cursor, height, highlightbackground, highlightcolor, highlightthickness, insertbackground, insertborderwidth, insertofftime, insertontime, insertwidth, offset, relief, scrollregion, selectbackground, selectborderwidth, selectforeground, state, takefocus, width, xscrollcommand, xscrollincrement, yscrollcommand, yscrollincrement.'''
        try:
            self._font = kwargs.get('font', ('Futura Hv BT', 14))
            kwargs.pop('font')
        except:
            ...
        super().__init__(master, **kwargs)
        
        self._kwargs = kwargs
        self._variables: dict[str, callable] = variables
        self._isNumbered = isNumbered
        self._rows: dict[int, tk.Frame] = {}
        self._columns: dict[str, tk.Label] = {}

        self.next_row = 0

        self._row_renders: dict[str, Image.Image] = {}

    def add(self, row: int, column: str, **kwargs):
        print(f'{row = } | {column = !s}')

        if row not in self._rows:
            if len(list(self._rows.items())) > 0:
                prev_row = self.value_frame.children[f'row_{row-1}_in_{column}']
                prev_row.update_idletasks()
                prev_row_height = prev_row.winfo_height() + prev_row.winfo_y()
            else:
                prev_row_height = 0

            self._rows[row] = tk.Frame(self.value_frame, background='lightgreen', name=f'row_{row}_in_{column}', highlightthickness=1, highlightbackground='#000')
            self._rows[row].place(x=-1, y=prev_row_height, relwidth=1)

            IDLabel = tk.Label(self._rows[row], text=row, font=self._font, name=f'_ID#{row}', width=5)
            IDLabel.pack(side=tk.LEFT, fill=tk.Y)
            IDLabel.update_idletasks()

        img = f'img_row_{row}_in_{column}'
        self._row_renders[img] = ImageTk.PhotoImage(self._variables[column](**kwargs))

        cell = tk.Label(self._rows[row], image=self._row_renders[img], anchor=tk.NW)
        cell.place(x=self._rows[row].children[f'_ID#{row}'].winfo_width(), 
                   relwidth=1/len(self._variables),
                   relx=(1/len(self._variables)) * list(self._variables.keys()).index(column))
        cell.update()
        self._rows[row].place(height=self.__heightest_cell(self._rows[row].children)+2)

    def __heightest_cell(self, row: dict[str, tk.Widget]):
        result = []
        
        for column in row:
            result.append(row[column].winfo_height())

        return max(result)

        
    def __render(self) -> None:
        self.update()
        if self._variables == None:
            return None
            
        header_frame = tk.Frame(self, name='header')
        header_frame.place(anchor=tk.NW, relwidth=1, height=30)

        if self._isNumbered:
            temp = tk.Label(header_frame, text=' No.', font=self._font, width=5, anchor=tk.NW, background=SECONDARY_COLOR)
            temp.place(x=0, relheight=1)
            temp.update()

        temp_current_relx = 0
        for text in self._variables:
            self._columns[text] = tk.Label(header_frame, text=text, font=self._font, anchor=tk.NW,background=SECONDARY_COLOR)
            self._columns[text].place(x=temp.winfo_width(), y=0, relheight=1, relwidth=1/len(self._variables), relx=temp_current_relx)
            temp_current_relx += 1/len(self._variables)

        header_frame.update()
        self.value_frame = tk.Canvas(self, bd=0, highlightthickness=0, name='body')
        self.value_frame.place(anchor=tk.NW, y=header_frame.winfo_height()+1, relheight=1, relwidth=1, height=-header_frame.winfo_height())

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



if __name__ == '__main__':

    WIDTH = 800
    HEIGHT = 500

    #~ Intialize window box
    window = Application()
    window.mainloop()
    opkSVG.clear()
