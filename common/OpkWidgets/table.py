import tkinter as tk
from tkinter import ttk
from typing import Callable

from common.OpkWidgets.row import Row
from common.OpkWidgets.button import Button
from common.Opkfilter import DataBaseDictFilter
from data.database.DBmanager import DataBase
from settings import SECONDARY_COLOR, PRIMARY_COLOR


class Table(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, *_, columns: dict[str, Callable] = None,
                 font: tuple[str, int] = None, display_number: bool = False, number_width: int = 3,
                 header_background: str | None = None, database: DataBase = None, **kwargs):
        super().__init__(master, **kwargs)

        self.columns = columns
        self.font = font if font else ('Futura Bk BT', 12)
        self.display_number = display_number
        self.number_width = number_width
        self.header_background = header_background if header_background else SECONDARY_COLOR
        self.body_background = self.cget('background')
        self.database: DataBase = database
        self.table = {}
        for table in self.database.get_table():
            self.table[table] = self.database.get_column(table, '*')

        # for t, v in DataBaseDictFilter(self.table, 'Volleyball').found().items():
        #     self.table[t] = {}
        #     index = 1
        #     for ky, it in v.items():
        #         self.table[t][index] = it
        #         index += 1

        self.create_column_header()

        if self.database:
            self.after(100, self.load_page, 1)

    def create_column_header(self) -> None:
        header_row = Row(self, background=self.header_background, name='header_row')

        if self.display_number:
            header_row.add_column_label(text='No.', param={'width': 5,
                                                           'font': ('Futura Hv BT', 18), 'background': 'red'},
                                        sticky='nw', weight=0, minsize=50)

        for col in self.columns:
            header_row.add_column_label(col, param={'width': self.number_width,
                                                    'font': (self.font[0], self.font[1]+2),
                                                    'anchor': tk.W,
                                                    'name': col.lower()})

    def load_page(self, page_num: int) -> None:
        frame_name = 'body_'
        if frame_name not in self.children:
            canvas = tk.Canvas(self, background='blue', name=frame_name+'canvas')
            # frame.pack(expand=True, fill=tk.BOTH, anchor=tk.NW)
            canvas.place(relwidth=1, y=self.children['header_row'].winfo_height(), relheight=1, height=-self.children['header_row'].winfo_height())
            # Add vertical scrollbar
            v_scrollbar = ttk.Scrollbar(canvas, orient=tk.VERTICAL, command=canvas.yview)
            v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Configure canvas scrolling
            canvas.configure(yscrollcommand=v_scrollbar.set)
            frame = tk.Frame(canvas, name=frame_name+'frame', height=100)
            tag = canvas.create_window((0, 0), window=frame, anchor="nw")

            # canvas.bind(
            #     "<Configure>",
            #     lambda e: (e.widget.itemconfig(tag, width=e.widget.winfo_width()), v_scrollbar.tkraise())
            # )

            frame.bind(
                '<Configure>',
                lambda e: (
                    canvas.configure(scrollregion=canvas.bbox("all")),
                )
            )
            canvas.bind(
                '<Configure>',
                lambda e: (
                    canvas.itemconfig(tag, width=canvas.winfo_width() - v_scrollbar.winfo_width())
                )
            )
        else:
            frame = self.children[frame_name+'frame']
            canvas = self.children[frame_name+'canvas']

        page_row = 10
        for i in range((page_row*(page_num-1)), page_row*page_num):
            if i == max(len(d) for n, d in self.table.items()):
                break
            row = Row(frame, background=self.body_background)
            if self.display_number:
                row.add_column_label(text=str(i+1),
                                     param={'width': 5,
                                            'font': ('Futura Hv BT', 18),
                                            'background': 'red'},
                                     sticky='nw', weight=0, minsize=50)

            for column, func in self.columns.items():
                widget = func(row, self.table['_'.join(column.split(' ')).upper()][i+1])
                row.add_column_window(widget)
            row.bind('<MouseWheel>', self.scroll_table)

        next_frame = tk.Frame(frame, background=self.body_background)
        next_frame.pack(expand=True, fill=tk.X, anchor=tk.NW)

        temp_frame = tk.Frame(next_frame)
        temp_frame.pack()
        max_prev = Button(temp_frame, text='<<', font=('Futura Hv BT', 24, 'bold'), background=PRIMARY_COLOR, width=3,
                          state=tk.DISABLED if page_num == 1 else tk.ACTIVE,
                          command=lambda: self.load_page(1),
                          radius=15, corners=(True, False, False, True))
        max_prev.pack(side=tk.LEFT)
        prev = Button(temp_frame, text='<', font=('Futura Hv BT', 24, 'bold'), background=PRIMARY_COLOR, width=3,
                      state=tk.DISABLED if page_num == 1 else tk.ACTIVE,
                      command=lambda p = page_num-1: self.load_page(p))
        prev.pack(side=tk.LEFT, padx=5)
        page = tk.Label(temp_frame, text = str(page_num), font=('Futura Hv BT', 24, 'bold'), background=PRIMARY_COLOR, width=3)
        page.pack(side=tk.LEFT, expand=True, fill=tk.Y, pady=2)
        next_ = Button(temp_frame, text='>', font=('Futura Hv BT', 24, 'bold'), background=PRIMARY_COLOR, width=3,
                       state=tk.DISABLED if page_row * page_num >= max(
                           len(d) for n, d in self.table.items()) else tk.ACTIVE,
                       command=lambda p = page_num+1: self.load_page(p))
        next_.pack(side=tk.LEFT, padx=5)
        max_next = Button(temp_frame, text='>>', font=('Futura Hv BT', 24, 'bold'), background=PRIMARY_COLOR, width=3,
                          state=tk.DISABLED if page_row * page_num >= max(
                              len(d) for n, d in self.table.items()) else tk.ACTIVE,
                          command=lambda p = page_num+1: self.load_page(max(len(d) for n, d in self.table.items())//page_row+1),
                          radius=15, corners=(False, True, True, False))
        max_next.pack(side=tk.LEFT)



    def scroll_table(self, event: tk.Event):
        canvas: tk.Canvas = self.children['body_canvas']
        if event.delta > 0:
            canvas.yview_scroll(-1, tk.UNITS)
        else:
            canvas.yview_scroll(1, tk.UNITS)

# Additional utility classes like Row, DataBase need to be defined for full functionality
