import tkinter as tk
from typing import Literal
from functools import lru_cache

class PersonalInformation(tk.Canvas):
    def __init__(self, master: tk.Misc | None, columns: dict, **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)

        self._default_font = ('Futura Bk BT', 16)
        self._heavy_font = ('Futura Hv BT', self._default_font[1]+2)
        self._tags = []

        self.max_height = self._default_font[1]*5*1.6
        self.configure(height=self.max_height)

        columns = {} if columns is None else columns
        name = ''
        if columns.get('First_Name', None) is not None:
            name += columns.get('First_Name')
        if columns.get('Middle_Name', None) is not None:
            name += ' ' + columns.get('Middle_Name')[0] + '.'
        if columns.get('Last_Name', None) is not None:
            name += ' ' + columns.get('Last_Name')
        if name == '':
            name = 'N/A'
        facebook_account: str = columns.get('Facebook_Account', 'N/A')
        sex: str = columns.get('Sex', 'N/A')
        age: str = columns.get('Age', '17+')
        birth: str = columns.get('Birth_Date', 'N/A')
        phone_num: str = columns.get('Phone_Number', 'N/A')
        school_id: str = columns.get('ID_Number', 'N/A')
        year_level: str = columns.get('Standing', 'N/A')
        admission_score: str = columns.get('Admission_Score', 'N/A')

        #* Column 1
        self._tags.append(self.text(10, 0, 'Name', font_type=0))
        self._tags.append(self.text(12, 28, name))

        self._tags.append(self.text(10, self.max_height-(28*2), 'Year Level', font_type=0))
        self._tags.append(self.text(12, self.max_height-28, year_level))
        # self._tags.append(self.text(10, self.max_height-28, 'Facebook Account', anchor=tk.SW, font_type=0))
        # self._tags.append(self.text(12, self.max_height, facebook_account, anchor=tk.SW))

        #* Column 2
        # column2_x = 0
        # for tag in self._tags:
        #     column2_x = max(column2_x, self.bbox(tag)[2])
        # column2_x += self._default_font[1] * 1.25
        # self._tags.append(self.text(column2_x, self.max_height*0,   f'Sex: {sex}'))
        # self._tags.append(self.text(column2_x, self.max_height*0.2, f'Age: {age}'))
        # self._tags.append(self.text(column2_x, self.max_height*0.4, f'Date of Birth: {birth}'))
        # self._tags.append(self.text(column2_x, self.max_height*0.6, f'Phone No.: {phone_num}'))
        # self._tags.append(self.text(column2_x, self.max_height*0.8, f'ID No.: {school_id}'))

        #* Column 1
        # column3_x = 0
        # for tag in self._tags:
        #     column3_x = max(column3_x, self.bbox(tag)[2])
        # column3_x += self._default_font[1] * 1.25
        # self._tags.append(self.text(column3_x, 0, 'Year Level', font_type=0))
        # self._tags.append(self.text(column3_x+2, 28, year_level))
        #
        # self._tags.append(self.text(column3_x, self.max_height-28, 'Admission Score', anchor=tk.SW, font_type=0))
        # self._tags.append(self.text(column3_x+2, self.max_height, admission_score, anchor=tk.SW))

        # maxWidth = 0
        # for tag in self._tags:
        #     maxWidth = max(maxWidth, self.bbox(tag)[2])
        # self.configure(width=maxWidth*1.25)

    @lru_cache
    def text(self, x: int | float = 0, y: int | float = 0, text: str = 'N/A', anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.NW, font_type: int = 1, fill: str = '#000'):
        return self.create_text(x, y, anchor=anchor, font=self._default_font if font_type else self._heavy_font, fill=fill, text=text)

class Specialization(tk.Canvas):
    def __init__(self, master: tk.Misc | None, columns: dict, **kwargs):
        super().__init__(master, highlightthickness=0, background='blue', **kwargs)

        if not columns:
            self.configure(width=0, height=0)
            return

        self._default_font = ('Futura Bk BT', 16)
        self._heavy_font = ('Futura Hv BT', self._default_font[1]+2)
        self._tags = []

        current_column = 10
        for column in columns:
            if column.lower() not in ['dance', 'sport', 'multimedia', 'literary', 'athletics', 'music', 'visual_art',
                                'programming_langauge', 'others']:
                self.configure(width=0, height=0)
                continue

            self._tags.append(self.text(current_column, 0, column.upper(), font_type=0))
            current_row = self._default_font[1] * 1.6
            for row in columns[column].split(', '):
                self._tags.append(self.text(current_column, current_row, f'• {row.title()}'))
                current_row += self._default_font[1] * 1.6

            for tag in self._tags:
                current_column = max(current_column, self.bbox(tag)[2])
            current_column += self._default_font[1] * 1.25
            self.configure(width=current_column, height=max(self.bbox(tag)[3] for tag in self._tags))

    @lru_cache
    def text(self, x: int | float = 0, y: int | float = 0, text: str = 'N/A', anchor: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = tk.NW, font_type: int = 1, fill: str = '#000'):
            return self.create_text(x, y, anchor=anchor, font=self._default_font if font_type else self._heavy_font, fill=fill, text=text)
