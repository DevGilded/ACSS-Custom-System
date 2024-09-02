import tkinter as tk
import pandas as pd
from common.OpkImage import image_text, combine_two_image
import common.Opktkinter as opk
import common.Opksvg as opkSVG

from PIL import Image
from tkinter import filedialog
from settings import *

def personal_info(**kwargs) -> Image:
    name: str = kwargs.get('name', 'N/A')
    facebook_account: str = kwargs.get('facebook_account', 'N/A')
    sex: str = kwargs.get('sex', 'N/A')
    age: str = kwargs.get('age', '17+')
    birth: str = kwargs.get('birth', 'N/A')
    phone_num: str = kwargs.get('phone_num', 'N/A')
    school_id: str = kwargs.get('school_id', 'N/A')
    year_level: str = kwargs.get('year_level', 'N/A')
    admission_score: str = kwargs.get('admission_score', 'N/A')

    resolution = 4

    default_font = FONT(FuturaBook, (14*TkinterFontModifiyer) * resolution)
    heavy_font = FONT(FuturaHeavy, (14*TkinterFontModifiyer) * resolution)

    main_img = Image.new('RGBA', (0, 0), '#FFF0')

    columns = {
        1: [image_text('Name ', heavy_font),
            image_text(name, default_font),
            image_text(' ', default_font),
            image_text('Facebook Account ', heavy_font),
            image_text(facebook_account, default_font)],
            
        2: [image_text(f'Sex: {sex}', default_font),
            image_text(f'Age: {age}', default_font),
            image_text(f'Date of Birth: {birth}', default_font),
            image_text(f'Phone Number: {phone_num}', default_font),
            image_text(f'ID: {school_id}', default_font)],
            
        3: [image_text('Year Level', heavy_font),
            image_text(year_level, default_font),
            image_text(' ', default_font),
            image_text('Admission Score [Freshman]', heavy_font),
            image_text(admission_score, default_font)]
    }

    for column in columns:
        column_img = Image.new('RGBA', (0, 0), '#fff0')

        for img in columns[column]:
            column_img = combine_two_image(column_img, img)

        main_img = combine_two_image(main_img, column_img, orientation='horizontal')

    return main_img.resize((round(main_img.size[0] / resolution), round(main_img.size[1] / resolution)))

def specialization(**kwargs) -> Image:
    resolution = 4

    default_font = FONT(FuturaBook, (14*TkinterFontModifiyer) * resolution)
    heavy_font = FONT(FuturaHeavy, (14*TkinterFontModifiyer) * resolution)

    main_img = Image.new('RGBA', (0, 0), '#fff')

    for variable in kwargs:
        if variable not in ['dance', 'sport', 'multimedia', 'literary', 'athletics', 'music', 'visual_art', 'others']:
            continue

        variable_img = Image.new('RGBA', (0, 0), '#fff')

        variable_img = combine_two_image(variable_img, image_text(variable.upper(), heavy_font))
        
        for value in kwargs[variable]:
            if type(value) is dict:
                key = list(value)[0]

                variable_img = combine_two_image(variable_img, image_text('  ' + key.title(), heavy_font))
                for value_ in value[key]:
                    ...
                    variable_img = combine_two_image(variable_img, image_text('  • ' + value_, default_font))

            else:
                ...
                variable_img = combine_two_image(variable_img, image_text('• ' + value, default_font))

        main_img = combine_two_image(main_img, variable_img, orientation='horizontal')

    return main_img.resize((round(main_img.size[0] / resolution), round(main_img.size[1] / resolution)))

def import_excel(event: tk.Event):
    filepath = filedialog.askopenfilename(
        title='Select a file',
        filetypes=(('Excel files', '*.xlsx'), ('All files', '*.*'))
    )
    if filepath:
        df = pd.read_excel(filepath, sheet_name='Book1')
        print(df)
        print(type(df))
        # with open(filepath, 'r') as f:
            # content = f.read()
            # print(content)

class Load:
    def __init__(self, master: tk.Frame) -> None:

        self.Widgets: dict[str, tk.Widget | opk.Table] = {
            'Filter': tk.Frame(master),
            'Button': tk.Frame(master),
            'Table': opk.Table(master,
                               variables = {'Personal Information': personal_info, 'Specialization': specialization},
                               font=('Futura Hv BT', 16)),
        }
        
        self.Widgets['Filter'].place(y=10, x=20)
        self.Widgets['Button'].place(y=10, x=-20, anchor='ne', relx=1)
        self.Widgets['Table'].place(x=20, relwidth=1, width=-40, y=60, relheight=1, height=-80)
        
        Specialization: dict = {
            'DANCE': ['Folkdance', {'Dance Sports': ['Latin', 'Standard']}, 'Modern/Street Dance', 'Contemporary Dance'],
            'SPORT': ['Volleyball','Basketball','Swimming','Soccer/Futsal','Lawn Tennis','Table Tennis','Badminton','Baseball/Softball','Takraw','Esports','Arnis','Taekwondo','Karatedo','Chess','Others'],
            'MULTIMEDIA': ['Graphics Designing', 'Videography/Filming', 'Photography', 'Others'],
            'LITERARY': ['Creative Writing', 'Extemporaneous \nSpeaking', 'Radio Drama', 'Dagliang Talumpati', 'Pagkukwento/Story \nRetelling', 'Biglaang Artista'],
            'ATHLETICS': ['Running Events', 'Jumping Events', 'Throwing Events'],
            'MUSIC': ['Singing', {'Instrumentalist': ['Guitarist', 'Pianist', 'Bassist', 'Drummer']}],
            'VISUAL ARTS': ['Poster Making', 'Cartooning', 'Painting', 'Pencil/Charcoal', 'Drawing', 'Mural Painting', 'Digital Painting', 'Others'],
            'OTHERS': ['Pageantry', 'Leadership', 'Craftmanship']
        }
        self.FilterWidget: dict[str, tk.Label | tk.OptionMenu] = {
            'Label': tk.Label(self.Widgets['Filter'], text='Filter by', font=('Futura Hv BT', 11)),
            'DropDown': opk.ComboBox(self.Widgets['Filter'], Specialization, text='-- Choose a Category --', font=('Futura Hv BT', 9), width=22, background=PRIMARY_COLOR, foreground=BLANK, activeforeground=BLANK, relief='sunken')
        }

        for widget in self.FilterWidget:
            self.FilterWidget[widget].pack(side=tk.LEFT)

        self.Icons: dict[str, str] = {
            'Print': opkSVG.ToPNG('assets/svg/print-icon.svg', 1.5),
            'Add': opkSVG.ToPNG('assets/svg/add-entry-icon.svg', 1.5),
            'Export': opkSVG.ToPNG('assets/svg/export-as-excel-icon.svg', 1.5),
        }

        self.ButtonWidget: dict[str, tk.Button] = {
            'PrintIcon': opk.Icon(self.Widgets['Button'], image=self.Icons['Print'], compound=tk.CENTER),
            'AddIcon': opk.Icon(self.Widgets['Button'], image=self.Icons['Add'], compound=tk.CENTER),
            'ExportIcon': opk.Icon(self.Widgets['Button'], image=self.Icons['Export'], compound=tk.CENTER),
            'S1': tk.Frame(self.Widgets['Button'], background='#333', height=30),
            'Edit': opk.Button(self.Widgets['Button'], text='Edit', font=('Futura Bk BT', 14), radius=30, width=12, background=SUCCES_COLOR),
            'Delete': opk.Button(self.Widgets['Button'], text='Delete', font=('Futura Bk BT', 14), radius=30, width=12, background=ERROR_COLOR)
        }

        for widget in self.ButtonWidget:
            self.ButtonWidget[widget].pack(side=tk.LEFT, anchor='w', padx=5, pady=1)

            match widget:
                case 'ExportIcon':
                    self.ButtonWidget[widget].bind('<Button>', import_excel)
                    self.ButtonWidget[widget].bind('<Enter>', lambda event, w = self.ButtonWidget[widget]: w.config(cursor='hand2'))
                    self.ButtonWidget[widget].bind('<Leave>', lambda event, w = self.ButtonWidget[widget]: w.config(cursor=''))
                case _:
                    ...

        for i in range(1, 20+1):
            self.Widgets['Table'].add(i, 'Personal Information', name='Mj Maruel L. Namok', facebookAccount = 'Mj Maruel Namok')
            self.Widgets['Table'].add(i, 'Specialization', dance=[
                                                                {'Dance Sports': [
                                                                    'Latin', 
                                                                    'Standard'
                                                                ]}, 
                                                                'Modern/Street Dance', 
                                                                'Contemporary Dance',
                                                            ],
                                                            sport=[
                                                                'Basketball',
                                                                'Soccer/Futsal',
                                                                'Lawn Tennis',
                                                                'Table Tennis',
                                                            ],
                                                            # others=[
                                                            
                                                            # ]
            ) 

        # for child in self.Widgets['Table'].value_frame.winfo_children():
        #     print(child)