import tkinter as tk
from typing import Literal

import common.Opktkinter as opk
from tkinter import ttk

import common.Opksvg as opkSVG
from PIL import ImageTk, Image

from common.OpkImage import create_circle
from settings import PRIMARY_COLOR, BLANK, SECONDARY_COLOR


class Row(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, x: int = 0, y: int = 0, **kwargs) -> None:
        super().__init__(master, **kwargs)

        self.columns = []
        self.is_selected = False

        # Place the frame itself in the master using grid
        # self.grid(row=y, column=x, sticky='nsew')
        self.pack(expand=True, fill=tk.X, anchor=tk.NW)

        # Separator to be placed below the row content
        self.separator = ttk.Separator(self, orient='horizontal')
        self.separator.grid(row=1, column=0, sticky='swe', columnspan=1, padx=10)

        # Configure the parent (master) row and column to make it expand
        self.master.grid_rowconfigure(y, weight=1)
        self.master.grid_columnconfigure(x, weight=1)

        self.bind('<Button-1>', self.select)

    def add_column_label(self, text: str = 'TEXT', *_, param=None,
                         sticky: str = 'nsew', weight: int = 1, minsize: int = 200, pady: float = 5, padx: float = 0):
        if param is None:
            param = {}

        column = tk.Label(self, text=text, **param)
        column.configure(background=self.cget('background'))
        column.grid(column=len(self.columns), row=0, sticky=sticky, pady=pady, padx=padx)
        self.columns.append(column)

        # Configure the column to expand within the row
        self.grid_columnconfigure(len(self.columns) - 1, weight=weight, minsize=minsize)

        # Update the separator's columnspan
        self.separator.grid(columnspan=len(self.columns))
        self.bind('<Button-1>', self.select)

    def add_column_window(self, window: tk.Widget, *_, sticky: str = 'nsew', weight: int = 1, minsize: int = 200,
                          pady: float = 5, padx: float = 0):
        window.configure(background=self.cget('background'))
        window.grid(column=len(self.columns), row=0, sticky=sticky, pady=pady, padx=padx)
        self.columns.append(window)

        # Configure the column to expand within the row
        self.grid_columnconfigure(len(self.columns) - 1, weight=weight, minsize=minsize)

        # Update the separator's columnspan
        self.separator.grid(columnspan=len(self.columns))
        self.bind('<Button-1>', self.select)

    def bind(
        self,
        sequence = None,
        func = None,
        add = None,
    ):
        super().bind(sequence, func, add)
        for i in self.children:
            # i.bind(sequence, func, add)
            self.nametowidget(i).bind(sequence, func, add)

    def select(self, event: tk.Event):
        if self.is_selected:
            print('Is Selected')
            self.edit_row_value()
            return
        else:
            for child in self.master.winfo_children():
                if isinstance(child, Row):
                    child.is_selected = False
        # print(event)

        select_color = PRIMARY_COLOR
        width = 2
        frame = tk.Frame(self.master, background=select_color, name='select_frame_left')
        frame.place(height=self.winfo_height(), y=self.winfo_y(), width=width)
        frame = tk.Frame(self.master, background=select_color, name='select_frame_top')
        frame.place(relwidth=1, y=self.winfo_y(), height=width, width=-1)
        frame = tk.Frame(self.master, background=select_color, name='select_frame_right')
        frame.place(height=self.winfo_height(), relx=1, x=-1, y=self.winfo_y(), width=width, anchor=tk.NE)
        frame = tk.Frame(self.master, background=select_color, name='select_frame_bottom')
        frame.place(relwidth=1, y=self.winfo_y()+self.winfo_height(), height=width, anchor=tk.SW, width=-1)

        self.is_selected = True

    def edit_row_value(self):
        canvas = tk.Canvas(background=BLANK, highlightbackground='black', name='row_form')
        canvas.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)
        canvas.update_idletasks()

        scroll_bar = tk.Scrollbar(command=canvas.yview)
        scroll_bar.place(relheight=0.9, height=-4, y=2, relx=0.95, x=-19, rely=0.05)
        scroll_bar.update_idletasks()
        canvas.configure(yscrollcommand=scroll_bar.set)
        canvas.config(scrollregion=(0,0,1000,10000))

        temp_image = ImageTk.PhotoImage(Image.open(opkSVG.ToPNG('assets/svg/cross-icon.svg', 2)))
        close_btn = canvas.create_image(canvas.winfo_width()-10-scroll_bar.winfo_width(), 10, anchor=tk.NE, image=temp_image)
        canvas.close_btn_image = temp_image

        padding = 20

        #FORM LAYOUT

        #HEADER
        #LOGO
        temp_image = ImageTk.PhotoImage(Image.open(opkSVG.ToPNG('assets/svg/CITE_Nemsu_tandag_Logo.svg', 2)))
        logo = canvas.create_image(padding+10, padding, anchor=tk.NW, image=temp_image)
        canvas.logo_image= temp_image

        #TITLES
        university = canvas.create_text(canvas.bbox(logo)[2]+padding, padding+5,
                                        text='North Eastern Mindanao State University - Tandag Campus', fill=PRIMARY_COLOR,
                                        anchor=tk.NW, font=('Garamond', 19, 'bold'))
        college = canvas.create_text(canvas.bbox(logo)[2]+padding, canvas.bbox(university)[3]-5,
                                     text='College of Information Technology Education', fill=PRIMARY_COLOR,
                                     anchor=tk.NW, font=('Franklin Gothic Heavy', 26, 'bold', 'italic'))
        course = canvas.create_text(canvas.bbox(logo)[2]+padding, canvas.bbox(college)[3]-5,
                                     text='Bachelor of Science in Computer Science', fill=PRIMARY_COLOR,
                                     anchor=tk.NW, font=('MonotypeOldEnglishTextW01', 28, 'bold'))
        address = canvas.create_text(canvas.bbox(logo)[2]+padding, canvas.bbox(course)[3]-5,
                                     text='Rosario, Tandag City, Surigao del Sur', fill=PRIMARY_COLOR,
                                     anchor=tk.NW, font=('EB Garamond', 19, 'italic'))
        x0, y0, x1, y1 = canvas.bbox(course)
        form_name_bc = canvas.create_rectangle(x0, y0+canvas.bbox(course)[1], x1, y1+canvas.bbox(course)[1], fill=SECONDARY_COLOR, width=0)
        form_name_txt = canvas.create_text((x0 + x1) / 2, (y0 + canvas.bbox(course)[1] + y1 + canvas.bbox(course)[1]) / 2,
                                     text='MEMBERSHIP FORM', fill=PRIMARY_COLOR,
                                     anchor=tk.CENTER, font=('Franklin Gothic Heavy', 32, 'bold'))

        sep1 = canvas.create_line(padding, canvas.bbox(logo)[3]+padding,
                                  canvas.winfo_width()-scroll_bar.winfo_width()-padding, canvas.bbox(logo)[3]+padding,
                                  fill='black')

        h1 = 22
        p1 = 19
        BLACK = 'black'
        #PERSONAL INFORMATION
        #Labels
        # column 1
        per_info_txt = canvas.create_text(padding, canvas.bbox(sep1)[3]+padding,
                                          text='Personal Information', fill=PRIMARY_COLOR,
                                          anchor=tk.NW, font=('Futura Hv BT', h1, 'bold'))
        last_name = CanvasWindow(canvas, (0, canvas.bbox(per_info_txt)[3]+padding),
                                 text='Last Name:', font=('Futura Bk BT', 19))
        middle_name = CanvasWindow(canvas, (0, canvas.bbox(int(last_name))[3]+padding),
                                 text='Middle Name:', font=('Futura Bk BT', 19))
        first_name = CanvasWindow(canvas, (0, canvas.bbox(int(middle_name))[3]+padding),
                                 text='First Name:', font=('Futura Bk BT', 19))
        facebook_account = CanvasWindow(canvas, (0, canvas.bbox(int(first_name))[3]+padding),
                                 text='Facebook Account:', font=('Futura Bk BT', 19))

        # last_name_label = canvas.create_text(padding, canvas.bbox(per_info_txt)[3]+padding,
        #                                      text='Last Name:', fill=BLACK,
        #                                      anchor=tk.NW, font=('Futura Bk BT', p1))
        # middle_name_label = canvas.create_text(padding, canvas.bbox(last_name_label)[3]+padding,
        #                                        text='Middle Name:', fill=BLACK,
        #                                        anchor=tk.NW, font=('Futura Bk BT', p1))
        # first_name_label = canvas.create_text(padding, canvas.bbox(middle_name_label)[3]+padding,
        #                                       text='First Name:', fill=BLACK,
        #                                        anchor=tk.NW, font=('Futura Bk BT', p1))
        # facebook_account_label = canvas.create_text(padding, canvas.bbox(first_name_label)[3]+padding,
        #                                       text='Facebook Account', fill=BLACK,
        #                                        anchor=tk.NW, font=('Futura Bk BT', p1))
        # # column 2
        # standing_label = canvas.create_text((canvas.winfo_width()*0.5)-padding, canvas.bbox(last_name_label)[1],
        #                                     text='Standing', fill=PRIMARY_COLOR,
        #                                     anchor=tk.NW, font=('Futura Bk BT', p1, 'bold'))
        # birthdate_label = canvas.create_text((canvas.winfo_width()*0.5)-padding, canvas.bbox(middle_name_label)[1],
        #                                      text='Birthdate:', fill=BLACK,
        #                                      anchor=tk.NW, font=('Futura Bk BT', p1))
        # age_label = canvas.create_text((canvas.winfo_width()*0.8)-padding, canvas.bbox(middle_name_label)[1],
        #                                text='Age:', fill=BLACK,
        #                                anchor=tk.NW, font=('Futura Bk BT', p1))
        # phone_num_label = canvas.create_text((canvas.winfo_width()*0.5)-padding, canvas.bbox(first_name_label)[1],
        #                                      text='Phone Number:', fill=BLACK,
        #                                      anchor=tk.NW, font=('Futura Bk BT', p1))
        # id_num_label = canvas.create_text((canvas.winfo_width()*0.65)-padding, canvas.bbox(facebook_account_label)[1],
        #                                   text='ID Number:', fill=BLACK,
        #                                   anchor=tk.NW, font=('Futura Bk BT', p1))
        #
        #
        # # column 1
        # #Entrys
        # # last_name_entry = canvas.create_window(canvas.bbox(last_name_label)[2]+padding,
        # #                                        canvas.bbox(last_name_label)[1],
        # #                                        anchor=tk.NW,
        # #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        # #                                        width=canvas.bbox(standing_label)[0] - canvas.bbox(last_name_label)[2] - padding)
        # middle_name_entry = canvas.create_window(canvas.bbox(middle_name_label)[2]+padding,
        #                                        canvas.bbox(middle_name_label)[1],
        #                                        anchor=tk.NW,
        #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                        width=canvas.bbox(birthdate_label)[0] - canvas.bbox(middle_name_label)[2] - padding)
        # first_name_entry = canvas.create_window(canvas.bbox(first_name_label)[2]+padding,
        #                                        canvas.bbox(first_name_label)[1],
        #                                        anchor=tk.NW,
        #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                        width=canvas.bbox(phone_num_label)[0] - canvas.bbox(first_name_label)[2] - padding)
        # facebook_account_entry = canvas.create_window(canvas.bbox(facebook_account_label)[2]+padding,
        #                                        canvas.bbox(facebook_account_label)[1],
        #                                        anchor=tk.NW,
        #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                        width=canvas.bbox(id_num_label)[0] - canvas.bbox(facebook_account_label)[2] - padding)
        #
        # # column 2
        # # Radio Button
        # x0, y0, x1, y1 = canvas.bbox(standing_label)
        # first_RB = CanvasRadioButton(canvas, (x1+padding/2, y0 + ((y1 - y0) / 2)), text='1st Year', font=('Futura Bk Hv', 10), anchor=tk.W)
        # second_RB = CanvasRadioButton(canvas,
        #                               (int(canvas.bbox(int(first_RB))[2]+padding/2), canvas.bbox(int(first_RB))[1]),
        #                               text='2nd Year',
        #                               font=('Futura Bk Hv', 10))
        # third_RB = CanvasRadioButton(canvas,
        #                              (int(canvas.bbox(int(second_RB))[2] + padding / 2), canvas.bbox(int(second_RB))[1]),
        #                              text='3rd Year',
        #                               font=('Futura Bk Hv', 10))
        # fourth_RB = CanvasRadioButton(canvas,
        #                               (int(canvas.bbox(int(third_RB))[2]+padding/2), canvas.bbox(int(third_RB))[1]),
        #                               text='4th Year',
        #                               font=('Futura Bk Hv', 10))
        # #Entrys
        # birthdate_entry = canvas.create_window(canvas.bbox(birthdate_label)[2]+padding,
        #                                        canvas.bbox(birthdate_label)[1],
        #                                        anchor=tk.NW,
        #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                        width=canvas.bbox(age_label)[0] - canvas.bbox(birthdate_label)[2] - padding)
        # age_label = canvas.create_window(canvas.bbox(age_label)[2]+padding,
        #                                  canvas.bbox(age_label)[1],
        #                                  anchor=tk.NW,
        #                                  window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                  width=canvas.bbox(int(fourth_RB))[2] - canvas.bbox(age_label)[2] - padding)
        # phone_num_entry = canvas.create_window(canvas.bbox(phone_num_label)[2]+padding,
        #                                        canvas.bbox(phone_num_label)[1],
        #                                        anchor=tk.NW,
        #                                        window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                        width=canvas.bbox(int(fourth_RB))[2] - canvas.bbox(phone_num_label)[2] - padding)
        # id_num_entry = canvas.create_window(canvas.bbox(id_num_label)[2]+padding,
        #                                     canvas.bbox(id_num_label)[1],
        #                                     anchor=tk.NW,
        #                                     window=tk.Entry(font=('Futura Bk BT', p1+2)),
        #                                     width=canvas.bbox(int(fourth_RB))[2] - canvas.bbox(id_num_label)[2] - padding)
        #
        sep2 = canvas.create_line(padding, canvas.bbox(logo)[3]+padding,
                                  canvas.winfo_width()-scroll_bar.winfo_width()-padding, canvas.bbox(logo)[3]+padding,
                                  fill='black')

        canvas.bind('<Configure>', lambda e: (
            canvas.coords(close_btn, e.width - 10 - scroll_bar.winfo_width(), canvas.bbox(close_btn)[1]),
            [canvas.coords(sep, padding, canvas.bbox(tag)[3] + padding,
                           canvas.winfo_width() - scroll_bar.winfo_width() - padding,
                           canvas.bbox(tag)[3] + padding) for sep, tag in {sep1: logo, sep2: logo}.items()]
        ))
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(-1, tk.UNITS) if e.delta > 0 else canvas.yview_scroll(1, tk.UNITS))
        canvas.tag_bind(close_btn, '<Button-1>', lambda e, c = canvas, s = scroll_bar: (c.place_forget(), s.place_forget()))

    def scroll_table(self, event: tk.Event):
        canvas: tk.Canvas = self.children['body_canvas']
        if event.delta > 0:
            canvas.yview_scroll(-1, tk.UNITS)
        else:
            canvas.yview_scroll(1, tk.UNITS)


class CanvasWindow:
    def __init__(self, canvas: tk.Canvas, xy: tuple[int, int], *_, text: str = '',
                 background: str = 'white', foreground: str = 'black',
                 font: any = ..., width: int | float = ...,
                 padding: int = 20, anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.NW) -> None:
        self.canvas: tk.Canvas = canvas
        self.text = text
        self.background = background
        self.foreground = foreground
        self.font = font
        self.width = width if width != Ellipsis else self.canvas.winfo_width()
        self.padding: int = padding
        self.anchor = anchor

        self.label = self.canvas.create_text(xy[0] + padding, xy[1],
                                             text=self.text, fill=self.foreground,
                                             anchor=self.anchor, font=self.font)

        self.entry = self.canvas.create_window(canvas.bbox(self.label)[2]+padding,
                                               canvas.bbox(self.label)[1] + ((canvas.bbox(self.label)[3] - canvas.bbox(self.label)[1]) / 2),
                                               anchor=tk.W,
                                               window=tk.Entry(self.canvas,
                                                               font=(self.font[0], self.font[1]+2, 'bold'),
                                               width=self.width - canvas.bbox(self.label)[2] - padding))

        self.box = self.canvas.create_rectangle(xy[0], xy[1],
                                                self.canvas.bbox(self.entry)[2], self.canvas.bbox(self.entry)[3],
                                                fill=self.background, width=0)
        self.canvas.lower(self.box)

    def __int__(self):
        return self.box

class CanvasRadioButton:
    def __init__(self, canvas: tk.Canvas, xy: tuple[int | float, int | float], text: str = '', font: any = ...,
                 background='white', anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.NW) -> None:
        self.canvas = canvas
        self.text = text
        self.font = font
        self.is_on = False

        # Store the image per instance, not in the canvas object
        self.fill_circle_image = ImageTk.PhotoImage(create_circle(background='black'))
        self.circle_image = ImageTk.PhotoImage(create_circle())

        # Create the circle (radio button)
        self.circle = self.canvas.create_image(xy[0], xy[1], anchor=anchor, image=self.circle_image)

        # Add text label
        padding = 4
        x0, y0, x1, y1 = self.canvas.bbox(self.circle)
        self.label = self.canvas.create_text(x1 + padding, y0 + ((y1 - y0) / 2), anchor=tk.W, text=text, font=font)

        # Create background box behind the text and circle
        _, _, x1, _ = self.canvas.bbox(self.label)
        self.box = self.canvas.create_rectangle(x0, y0, x1, y1, fill=background, width=0)
        self.canvas.lower(self.box)

        # Bind click events for the circle and label
        self.canvas.tag_bind(self.circle, '<Button-1>', self.onclick)
        self.canvas.tag_bind(self.label, '<Button-1>', self.onclick)

    def __int__(self):
        return self.box

    def onclick(self, event: tk.Event) -> None:
        if self.is_on:
            self.canvas.itemconfigure(self.circle, image=self.circle_image)
            self.is_on = False
        else:
            self.canvas.itemconfigure(self.circle, image=self.fill_circle_image)
            self.is_on = True



