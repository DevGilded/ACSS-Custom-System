import tkinter as tk

import pandas
import pandas as pd

from common.OpkFunc import PersonalInformation, Specialization
import common.Opktkinter as opk
import common.Opksvg as opkSVG
from data.database.DBmanager import add_value, get_ID, get_rows, get_value, DataBase

from PIL import Image
from tkinter import filedialog
from settings import *

def import_excel(event: tk.Event):
    filepath = filedialog.askopenfilename(
        title='Select a file',
        filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
    )
    if filepath:
        df = pd.read_excel(filepath, sheet_name='Book1')
        for row in range(max(df.count())):
            add_value('data/database/member.db', 'PERSONAL_INFORMATION',
                      Last_Name = get_column_value(df, 'Last Name', row),
                      Middle_Name = get_column_value(df, 'Middle Name', row),
                      First_Name = get_column_value(df, 'First Name', row),
                      Email_Address = get_column_value(df, 'Email Address', row),
                      Standing = get_column_value(df, 'Standing (Year Level)', row),
                      Facebook_Account = get_column_value(df, 'Facebook Account', row),
                      Birth_Date = get_column_value(df, 'Birthdate', row),
                      Age = get_column_value(df, 'Age', row),
                      Phone_Number = get_column_value(df, 'Phone Number', row),
                      ID_Number = get_column_value(df, 'ID Number', row),
                      Admission_Score = get_column_value(df, 'Entrance Exam Result', row))

            ID = get_ID('data/database/member.db', 'PERSONAL_INFORMATION',
                         Last_Name = get_column_value(df, 'Last Name', row),
                         First_Name = get_column_value(df, 'First Name', row))

            add_value('data/database/member.db', 'QUESTIONS',
                      PI_ID = ID,
                      Q1 = get_column_value(df, 'Q1. Do you have a basic computer background?', row),
                      A1 = get_column_value(df, 'if yes, write something about it.', row),
                      Q2 = get_column_value(df, 'Q2. Do you have an awareness of any programming languages?', row),
                      A2 = get_column_value(df, 'if yes, write something about it.', row),
                      Q3 = get_column_value(df, 'Q3. Do you have a laptop/desktop computer that you can use?', row),
                      A3 = get_column_value(df, 'On the scale of 1 to 10, rate your expected difficulty level of the BSCS program.', row),
                      Q4 = get_column_value(df, 'Have you ever participated in High-level Competitions?', row),
                      A4 = get_column_value(df, 'if yes, write something about it, number it if you have multiple experiences.', row),
                      Q5 = get_column_value(df, 'if you choose leadership, provide at least 4 leadership backgrounds (number it 1 to 4).', row),
                      A5 = get_column_value(df, 'What are your other skills & talents?', row))

            add_value('data/database/member.db', 'SPECIALIZATION',
                      PI_ID = ID,
                      DANCE = get_column_value(df, 'DANCE', row),
                      SPORT = get_column_value(df, 'SPORTS', row),
                      MULTIMEDIA = get_column_value(df, 'MULTIMEDIA', row),
                      LITERARY = get_column_value(df, 'LITERARY', row),
                      ATHLETICS = get_column_value(df, 'ATHLETICS', row),
                      MUSIC = get_column_value(df, 'MUSIC', row),
                      VISUAL_ARTS = get_column_value(df, 'VISUAL ARTS', row),
                      PROGRAMMING_LANGUAGE = get_column_value(df, 'PROGRAMMING LANGUAGE/S KNOWN', row),
                      OTHERS = get_column_value(df, 'OTHERS', row))

def value_to_param(param, val, sub = None):
    result = {param: []}
    # for value in str(val).split(', '):
    #     result[param].append(value)

    sub_param = {}
    if sub is not None:
        sub_param = {sub: []}

    for value in str(val).split(', '):
        if value != sub:
            result[param].append(value)
        if sub is not None:
            print(value)
            sub_param[sub].append(value)

    if sub is not None:
        print(sub_param[sub])
        if len(sub_param[sub]):
            result[param].append(sub_param)

    return result

def row_cases(match_name, val):
    result = {}
    match match_name:
        case 'DANCE':
            result['dance'] = []
            for value in str(val).split(', '):
                if value[0:14] == 'Dance Sports: ':
                    result['dance'].append({'Dance Sports': [value[14::]]})
                else:
                    result['dance'].append(value)
        case 'SPORT':
            result.update(value_to_param('sport', val))
        case 'MULTIMEDIA':
            result.update(value_to_param('multimedia', val))
        case 'LITERARY':
            result.update(value_to_param('literary', val))
        case 'ATHLETICS':
            result.update(value_to_param('athletics', val))
        case 'MUSIC':
            result.update(value_to_param('music', val, 'instrumentalist'))
            # result['music'] = []
            # instrument = {'instrumentalist': []}
            # for value in str(val).split(', '):
            #     if value == 'Singing':
            #         result['music'].append(value)
            #     else:
            #         instrument['instrumentalist'].append(value)
            # if len(instrument['instrumentalist']):
            #     result['music'].append(instrument)
        case 'VISUAL_ARTS':
            result.update(value_to_param('visual_art', val))
        case 'PROGRAMMING_LANGUAGE':
            result.update(value_to_param('programming_langauge', val))
        case 'OTHERS':
            result.update(value_to_param('others', val))
    return result

def table_to_param(row):
    result = {}
    for key, val in row.items():
        if val is None or key in ['ID', 'PI_ID']:
            continue
        result.update(row_cases(key, val))
    return result

def get_column_value(excelfile, column: str, row: int):
    # print(column)
    result = list(excelfile.get(column))[row]

    if type(result) is pandas.Timestamp:
        result = str(result)[0:9]

    return result


class Load:
    def __init__(self, master: tk.Frame) -> None:

        database = DataBase('data/database/member.db')

        self.Layout: dict[str, tk.Frame] = {
            'Ribbon': tk.Frame(master),
            'Body': tk.Frame(master)
        }

        ## RIBBON ##
        self.Layout['Ribbon'].place(relwidth=1, height=80)

        self.RibbonLayout: dict[str, tk.Frame] = {
            'Left': tk.Frame(self.Layout['Ribbon']),
            'Right': tk.Frame(self.Layout['Ribbon']),
        }

        ### LEFT ###
        self.RibbonLayout['Left'].place(relwidth=0.60, relheight=1, rely=0.5, x=5, width=-10, height=-10, anchor = tk.W)

        self.Filter: dict[str, tk.Widget] = {
            'Label': tk.Label(self.RibbonLayout['Left'], text='Filter by', font = ('Futura Hv BT', 16)),
            'Button': opk.ComboBox(self.RibbonLayout['Left'],
                                   text = '-- Choose a Category --',
                                   font = ('Futura Hv BT', 12),
                                   show_selected = True,
                                   combo_param= {'foreground': BLANK,
                                                 'activeforeground': BLANK,
                                                 'radius': 10,
                                                 'background': PRIMARY_COLOR,
                                                 'width': 22
                                   },
                                   values=[{'text': 'DANCE',
                                            'values': ['Folk dance',
                                                       {'text': 'DANCE',
                                                        'values': ['Latin', 'Standard'],
                                                        'font': ('Futura Hv BT', 12),
                                                        'value_type': 'check'},
                                                       'Modern/Street Dance',
                                                       'Contemporary Dance'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'SPORT',
                                            'values': ['Volleyball', 'Basketball', 'Swimming', 'Soccer/Futsal', 'Lawn Tennis', 'Table Tennis',
                                                       'Badminton', 'Baseball/Softball', 'Takraw', 'Esports', 'Arnis', 'Taekwondo', 'Karatedo', 'Chess',
                                                       '[SPORT] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'MULTIMEDIA',
                                            'values': ['Graphics Designing', 'Videography/Filming', 'Photography', '[MULTIMEDIA] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'ATHLETICS',
                                            'values': ['Running Events', 'Jumping Events', 'Throwing Events', '[ATHLETICS] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'MUSIC',
                                            'values': ['Singing',
                                                       {'text': 'Instrumentalist',
                                                        'values': ['Guitarist', 'Pianist', 'Bassist', 'Drummer'],
                                                        'font': ('Futura Hv BT', 12),
                                                        'value_type': 'check'},
                                                       '[MUSIC] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'VISUAL ARTS',
                                            'values': ['Poster Making', 'Cartooning', 'Painting', 'Pencil/Charcoal', 'Drawing', 'Mural Painting',
                                                        'Digital Painting', '[VISUAL ARTS] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'},
                                           {'text': 'OTHERS',
                                            'values': ['Pageantry', 'Leadership', 'Craftsmanship', '[OTHERS] Others'],
                                            'font': ('Futura Hv BT', 12),
                                            'value_type': 'check'}
                                   ]
            )
        }

        for widget in self.Filter:
            self.Filter[widget].pack(side=tk.LEFT, anchor='w', padx=5, pady=1)

        ### RIGHT ###
        self.RibbonLayout['Right'].place(relwidth=0.40, relheight=1, rely=0.5, relx=1, x=-5, width=-10, height=-10, anchor = tk.E)

        self.Icons: dict[str, str] = {
            'Print': opkSVG.ToPNG('assets/svg/print-icon.svg', 1.75),
            'Add': opkSVG.ToPNG('assets/svg/add-entry-icon.svg', 1.75),
            'Export': opkSVG.ToPNG('assets/svg/export-as-excel-icon.svg', 1.75),
        }

        self.ButtonWidget: dict[str, tk.Button] = {
            'Delete': opk.Button(self.RibbonLayout['Right'], text='Delete', font=('Futura Bk BT', 15), radius=30, width=12, background=ERROR_COLOR),
            'Edit': opk.Button(self.RibbonLayout['Right'], text='Edit', font=('Futura Bk BT', 15), radius=30, width=12, background=SUCCES_COLOR),

            'S1': tk.Frame(self.RibbonLayout['Right'], background='#333', height=35),
            'PrintIcon': opk.Icon(self.RibbonLayout['Right'], image=self.Icons['Print'], compound=tk.CENTER),
            'AddIcon': opk.Icon(self.RibbonLayout['Right'], image=self.Icons['Add'], compound=tk.CENTER),
            'ExportIcon': opk.Icon(self.RibbonLayout['Right'], image=self.Icons['Export'], compound=tk.CENTER),
        }

        for widget in self.ButtonWidget:
            self.ButtonWidget[widget].pack(side=tk.RIGHT, anchor='w', padx=5, pady=1)

            match widget:
                case 'ExportIcon':
                    self.ButtonWidget[widget].bind('<Button>', import_excel)
                    self.ButtonWidget[widget].bind('<Enter>', lambda event, w = self.ButtonWidget[widget]: w.config(cursor='hand2'))
                    self.ButtonWidget[widget].bind('<Leave>', lambda event, w = self.ButtonWidget[widget]: w.config(cursor=''))
                case _:
                    ...

        ## BODY ##
        self.Layout['Body'].place(relwidth=1, height=-80, relheight=1, y=80)

        self.Table: opk.Table = opk.Table(self.Layout['Body'],
                       columns = {
                           'Personal Information': PersonalInformation,
                           'Specialization': Specialization},
                       display_number=True,
                       database=database,
                       font=('Futura Hv BT', 16))
        self.Table.place(x=10, relwidth=1, width=-20, y=10, relheight=1, height=-20)

        # self.Widgets: dict[str, tk.Widget | opk.Table] = {
        #     'Filter': tk.Frame(master, background='lightgreen'),
        #     'Button': tk.Frame(master),
        #     'Table': opk.Table(master,
        #                        variables = {'Personal Information': personal_info, 'Specialization': specialization},
        #                        value=database,
        #                        font=('Futura Hv BT', 16)),
        # }
        #
        # self.Widgets['Filter'].pack(anchor = tk.NW, pady=15, padx=25)
        # self.Widgets['Button'].place(y=10, x=-20, anchor='ne', relx=1)
        #
        # specialization_list: list = [
        #     {'DANCE': ['Folkdance', {'text': 'Dance Sports', 'values' : ['Latin', 'Standard']}, 'Modern/Street Dance',
        #                'Contemporary Dance']},
        #     {'SPORT': ['Volleyball', 'Basketball', 'Swimming', 'Soccer/Futsal', 'Lawn Tennis', 'Table Tennis',
        #                'Badminton', 'Baseball/Softball', 'Takraw', 'Esports', 'Arnis', 'Taekwondo', 'Karatedo', 'Chess',
        #                'Others']},
        #     {'MULTIMEDIA': ['Graphics Designing', 'Videography/Filming', 'Photography', 'Others']},
        #     {'LITERARY': ['Creative Writing', 'Extemporaneous \nSpeaking', 'Radio Drama', 'Dagliang Talumpati',
        #                   'Pagkukwento/Story \nRetelling', 'Biglaang Artista']},
        #     {'ATHLETICS': ['Running Events', 'Jumping Events', 'Throwing Events']},
        #     {'MUSIC': ['Singing', {'text': 'Instrumentalist', 'values': ['Guitarist', 'Pianist', 'Bassist', 'Drummer']}]},
        #     {'VISUAL ARTS': ['Poster Making', 'Cartooning', 'Painting', 'Pencil/Charcoal', 'Drawing', 'Mural Painting',
        #                      'Digital Painting', 'Others']},
        #     {'OTHERS': ['Pageantry', 'Leadership', 'Craftmanship']}
        # ]
        # self.FilterWidget: dict[str, tk.Label | tk.OptionMenu] = {
        #     'Label': tk.Label(self.Widgets['Filter'], text='Filter by', font=('Futura Hv BT', 11)),
        #     'DropDown': opk.ComboBox(self.Widgets['Filter'])
        # }
        #
        # for widget in self.FilterWidget:
        #     self.FilterWidget[widget].pack()
        #

        #

        #
        # self.Widgets['Table'].place(x=20, relwidth=1, width=-40, y=60, relheight=1, height=-80)
