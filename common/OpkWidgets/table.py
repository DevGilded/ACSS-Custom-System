import tkinter as tk

from typing import Callable
from PIL import Image, ImageTk
from functools import lru_cache
from settings import *

class Table(tk.Canvas):
    def __init__(self, master: tk.Misc | None = None, variables: list[str, Callable] | None = None,
                 is_numbered: bool = True, **kwargs):
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
                prev_row = self.value_frame.children[f'row_{row - 1}_in_{column}']
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
                   relwidth=1 / len(self._variables),
                   relx=(1 / len(self._variables)) * list(self._variables.keys()).index(column),
                   anchor=tk.W,
                   rely=0.5)
        cell.update_idletasks()
        cell.bind('<MouseWheel>', self.scroll_table)
        self._rows[row].place(height=self.__heightest_cell(self._rows[row].children) + 5)

        self.value_frame.config(height=self._rows[row].winfo_height() + self._rows[row].winfo_y() + 20,
                                width=self._rows[row].winfo_width() + self._rows[row].winfo_x())
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
            temp = tk.Label(header_frame, text=' No.', font=self._font, width=5, anchor=tk.NW,
                            background=SECONDARY_COLOR, name='number')
            temp.place(x=0, relheight=1)
            temp.update()

        temp_current_relx = 0
        for text in self._variables:
            self._columns[text] = tk.Label(header_frame, text=text, font=self._font, anchor=tk.NW,
                                           background=SECONDARY_COLOR)
            self._columns[text].place(x=header_frame.children['number'].winfo_width(), y=0, relheight=1,
                                      relwidth=1 / len(self._variables), relx=temp_current_relx)
            temp_current_relx += 1 / len(self._variables)

        header_frame.update()
        self.value_canvas = tk.Canvas(self, bd=0, highlightthickness=0, name='body', background='#aaa')
        self.value_canvas.place(anchor=tk.NW, y=header_frame.winfo_height() + 1, relheight=1, relwidth=1,
                                height=-header_frame.winfo_height())

        self.value_frame = tk.Frame(self.value_canvas, bd=0, highlightthickness=0, name='body', background='#aaa',
                                    width=header_frame.winfo_width())
        # self.value_frame.place(anchor=tk.NW, y=header_frame.winfo_height()+1, relheight=1, relwidth=1, height=-header_frame.winfo_height())

        self.value_canvas.create_window((0, 0), window=self.value_frame, anchor=tk.NW)

        self.vsb = tk.Scrollbar(self, orient='vertical', command=self.value_canvas.yview)
        # self.vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.value_canvas.configure(yscrollcommand=self.vsb.set)

        header_frame.bind('<Configure>', self.dynamic_change)
        self.value_frame.bind('<MouseWheel>', self.scroll_table)

    @lru_cache
    def scroll_table(self, event: tk.Event):
        self.value_canvas.yview_scroll(int(-1 * (event.delta / 120)), tk.UNITS)

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