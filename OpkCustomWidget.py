'''
    What's Wrong with this code cause every time I remove/comment line 81 the text won't show up?
'''
import tkinter as tk
import tkinter.ttk as ttk
import cairosvg
import time

from PIL import Image, ImageTk, ImageDraw, ImageFont
from settings import *
from typing import Literal


class Opk:
    def __init__(self, canvas: tk.Canvas) -> None:
        canvas.update()
        self.canvas = canvas

    def place(self, y=0, x=0,rely:float=0,relx:float=0):
        self.ID = self.canvas.create_image((self.canvas.winfo_width()/2) - (self.width/2) if x == 0 else x, y, anchor=tk.NW, image=self.photo_image)
        self.canvas.image = self.photo_image

class Label(Opk):
    def __init__(self, canvas: tk.Canvas, text: str, font: ImageFont.truetype, border: float = 0, width: int = 0, height: int = 0, foreground: str = ..., background: str = ..., outline: str = ..., radius: float = 0, padding: tuple[int, int] | int = 0) -> None:
        super().__init__(canvas)
        # Text
        self._text = str(text)
        self._font = font

        # Text Size
        self._bbox = self._font.getbbox(self._text)
        
        # Size
        self._border = border
        if type(padding) == int:
            self._padding = [padding, padding]
        else:
            self._padding = padding
        self._width = (width if width > (self._bbox[2] - self._bbox[0]) else (self._bbox[2] - self._bbox[0])) + self._padding[0]*2
        self._height = (height if height > (self._bbox[3] - self._bbox[1]) else (self._bbox[3] - self._bbox[1])) + self._padding[1]*2
        self._radius = radius
        # Color
        self._foreground = foreground if foreground != ... else '#000'
        self._background = background
        self._outline = outline if outline != ... else '#000'
        # Boolean
        self.__isPlaced = False  
        
        self._rect = Image.new('RGBA', (
                                self._width,
                                self._height
                                ), '#0000')

    def change_text(self, text):
        bbox = self.canvas.bbox(self.ID)
        self._width = self._font.getbbox(text)[2] + self._padding[0]*2
        self._height = self._font.getbbox(text)[3] + self._padding[1]*2
        self.canvas.delete(self.ID)
        self._rect = Image.new('RGBA', (
                                self._width,
                                self._height
                                ), '#f000')
        self._text = text
        self.__create_text
        self._render = ImageTk.PhotoImage(self._rect)
        self.ID = self.canvas.create_image(bbox[0], bbox[1], anchor=self._anchor, image=self._render)

    def __create_text(self):
        draw = ImageDraw.Draw(self._rect)
        draw.text((self._padding[0], -self._bbox[1]+self._padding[1]), text=self._text, fill=self._foreground if self._foreground != ... else '#0000', font=self._font)

    def __create_background(self):
        draw = ImageDraw.Draw(self._rect)
        draw.rounded_rectangle((0,0,self._width+(self._padding[0]*2)-1, self._height+(self._padding[1]*2)-1), 
                               radius = self._radius, 
                               fill = '#0000'  if self._background == ... else self._background, 
                               outline ='#000' if self._outline == ... else self._outline,
                               width = self._border)

    def place(self, y=0, x=0,rely:float=0,relx:float=0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw'):
        self.canvas.update()
        self._anchor = anchor
        self.__create_background()
        self.__create_text()
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx), y+(self.canvas.winfo_height()*rely), anchor=self._anchor, image=self._render)
        self.canvas.bind('<Configure>', lambda event: self.place(y, x, rely, relx, anchor))
            
    def dynamicChange(self, event):
        pass

class Icon(Opk):
    def __init__(self, canvas: tk.Canvas, image: str, name: str = ..., scale: int = 1, command: callable = ..., output_height: any = None, output_width: any = None) -> None:
        super().__init__(canvas)
        if image.split('.')[-1] == 'svg':
            try:
                self._image_name = image.split('/')[-1].split('.')
            except:
                pass

            cairosvg.svg2png(url=image, write_to=f'assets/svg_to_png/{self._image_name[0]}.png', scale=scale, output_height=output_height, output_width=output_width)
            self._image_path = f'assets/svg_to_png/{self._image_name[0]}.png'
        else:
            self._image_path = image

        self._name = name

        self.command = command if command != ... else 'No Command Set'

        self._rect = Image.open(self._image_path)


    def __on_motion(self, event):
        self.canvas.tag_raise(self._display_ID)
        self.canvas.itemconfig(self._display_ID, anchor='nw')
        self.canvas.move(self._display_ID, -self.canvas.bbox(self._display_ID)[0], -self.canvas.bbox(self._display_ID)[1])
        self.canvas.move(self._display_ID, event.x-(self.canvas.bbox(self._display_ID)[2]/2), event.y-18)

    def leaveArea(self, event):
        event.widget.config(cursor='')

        if self._name != ...:
            self.canvas.itemconfig(self._display_ID, anchor='se')
            self.canvas.move(self._display_ID, -9999, -9999)

    def place(self, y=0, x=0,rely:float=0,relx:float=0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw'):
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx), y+(self.canvas.winfo_height()*rely), anchor=anchor, image=self._render)
        self.canvas.tag_bind(self.ID, '<Button-1>', self.command)
        
        self.canvas.tag_bind(self.ID, '<Enter>', lambda event: event.widget.config(cursor='hand2'))
        self.canvas.tag_bind(self.ID, '<Leave>', self.leaveArea)

        if self._name != ...:
            self._display_name = tk.Label(self.canvas,text=self._name, state='disabled')

            font = FONT(FuturaBook, 14)
            _, _, right, bottom = font.getbbox(self._name)
            self._text_rect = Image.new('RGBA', (right, bottom), '#fff0')
            draw = ImageDraw.Draw(self._text_rect)
            draw.text([0,0], text=self._name, fill='#333', font=font)
            self._text_render = ImageTk.PhotoImage(self._text_rect)
            self._display_ID = self.canvas.create_image(0,0, anchor='se', image=self._text_render)

            self.canvas.tag_bind(self.ID, '<Motion>', self.__on_motion)

class Entry(Opk):
    def __init__(self, canvas: tk.Canvas, displayText = ..., font: ImageFont.truetype = ..., 
                 width: int = 20, height: int = 0, foreground: str = ..., background: str = ..., 
                 outline: str = ..., padding: int | tuple[int, int] = 0, border: int=1, radius: int=...,
                 textVariable: tk.Variable = ..., variableLimit: int = ..., isCalendar: bool = ...) -> None:
        super().__init__(canvas)
        #~ Boolean
        self._isCalendar = isCalendar if isCalendar != ... else False
        self._showCalendar = False
        #~ Text
        self._displayText = (displayText if displayText != ... else '') if textVariable == ... else textVariable.get()
        self._font = font if font != ... else FONT(FuturaBook, 12)
        self._fontSize = self._font.getbbox('W')[3] if font != ... else 12
        self._textVariable = textVariable if textVariable != ... else tk.StringVar()
        self._textVariable.set(self._displayText)
        if variableLimit != ... or self._isCalendar:
            self._textVariable.trace_add('write', self.__on_text_change)
        # print(type(self._textVariable), tk.IntVar, ' ', (self._entry.winfo_height() if type(self._textVariable) == tk.IntVar() else 0))
        #~ Size
        if type(padding) == tuple:
            self._padding = [padding[0]+1, padding[1]+1]
        else:
            self._padding = [padding+1, padding+1]
        self._border = border
        self._radius = radius
        self._width = width
        self._height = height
        self._textLimit = variableLimit
        #~ Color
        self._foreground = foreground if foreground != ... else '#000'
        self._background = background if background != ... else '#fff'
        self._outline = outline if outline != ... else '#000'

        #~ Preload
        self.__create_entry()
        self._width = self._entry.winfo_width() + (self._padding[0]*2) + (self._entry.winfo_height() if radius == ... else radius)  + (self._entry.winfo_height() if type(self._textVariable) == tk.IntVar or self._isCalendar else 0)
        self._height = max(self._entry.winfo_height(), height) + (self._padding[1]*2)
        self._rect = Image.new('RGBA',
                               (
                                   self._width,
                                   self._height
                               ),
                               '#0000')

    def __on_text_change(self, var, index, mode):
        if type(self._textVariable) == tk.IntVar:
            try:
                self._textVariable.set(min(self._textVariable.get(), self._textLimit))
                return 0
            except:
                pass

        if self._isCalendar:
            content = self._textVariable.get()
            words = []
            for l in str(content):
                if l == '-':
                    continue
                if type(self._textVariable) == tk.IntVar:
                    words.append(int(l))
                else:
                    words.append(l)
            if len(words) >= 8:
                date = ''
                for day in words[:2]:
                    if day != '-':
                        date += str(day)
                if words[3] != '-':
                    date += '-'
                for month in words[2:4]:
                    if month != '-':
                        date += str(month)
                if words[5] != '-':
                    date += '-'
                for year in words[4:8]:
                    if month != '-':
                        date += str(year)
                self._textVariable.set('')
                self._textVariable.set(date)
                self._entry.icursor(len(date))
            return 0

        try:
            content = self._textVariable.get()
            words = []
            for l in str(content):
                if type(self._textVariable) == tk.IntVar:
                    words.append(int(l))
                else:
                    words.append(l)
            if len(words) > self._textLimit:
                result = ''
                for l in range(self._textLimit):
                    result += str(words[l])
                if type(self._textVariable) == tk.IntVar:
                    result = int(result)
                self._textVariable.set(result)
            return 0
        except:
            pass

    def __create_entry(self):
        self._entry = tk.Entry(self.canvas, relief='flat', width=self._width, background=self._background, foreground='gray75' if type(self._textVariable) == tk.StringVar and self._displayText != ... else '#000',
                               font=(self._font.path, self._fontSize), textvariable=self._textVariable)
        self._entry.place(y=0, x=0)
        self._entry.update()
        self._entry.place(y=-self._entry.winfo_height(), x=-self._entry.winfo_width()-(self._entry.winfo_height() if type(self._textVariable) == tk.IntVar else 0))
        self._entry.bind('<FocusIn>', lambda event: (self._entry.configure(foreground=self._foreground), self._textVariable.set('') if self._textVariable.get() == self._displayText else ...))
        self._entry.bind('<FocusOut>', self.__FocusOut)

    def __FocusOut(self, event):
        try:
            if self._textVariable.get() == '':
                self._textVariable.set(self._displayText)
                self._entry.configure(foreground='gray75') 
        except:
            self._textVariable.set(self._displayText)

    def __create_background(self):
        draw = ImageDraw.Draw(self._rect)
        draw.rounded_rectangle((0,0,self._width-1, self._height-1),
                                width=self._border, radius=self._height/2 if self._radius == ... else self._radius,
                                fill=self._background, outline=self._outline)

    def __show_calendar(self, event):
        if not self._showCalendar:
            self._calendar = Create_Calendar(self, self.canvas, FONT(FuturaBook, int(self._height/1.5)-5))
            self._calendar.place(y=self.canvas.bbox(self.ID)[3],
                                x=self.canvas.bbox(self.ID)[0],
                                width=self._width)
            self._showCalendar = True
        else:
            self._calendar.destroy()
            self._showCalendar = False

    def __up_down(self, event):
        iconBbox = self.canvas.bbox(self._icon.ID)
        if event.y < iconBbox[3]-((iconBbox[3]-iconBbox[1])/2):
            if self._textVariable.get() < self._textLimit:
                self._textVariable.set(self._textVariable.get()+1)
        else:
            if self._textVariable.get() > 0:
                self._textVariable.set(self._textVariable.get()-1)

    def place(self, y=0, x=0, rely: float = 0, relx: float = 0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw'):
        self.__create_background()
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx), y+(self.canvas.winfo_height()*rely), anchor=anchor, image=self._render)
        
        self._entry.place(x=self.canvas.bbox(self.ID)[0]+self._padding[0]+(self._rect.size[0]/2)-(self._entry.winfo_width()/2)-1-(self._entry.winfo_height()/2 if type(self._textVariable) == tk.IntVar or self._isCalendar else 0), 
                          y=self.canvas.bbox(self.ID)[1]+self._padding[1]+(self._rect.size[1]/2)-(self._entry.winfo_height()/2)-1,
                            anchor='nw')
        
        if type(self._textVariable) == tk.IntVar:
            self._icon = Icon(self.canvas, 'assets/svg/up-down-icon.svg', output_height=self._entry.winfo_height()-10, output_width=self._entry.winfo_height()-10, command=self.__up_down)
            self._icon.place(x=self._entry.winfo_width()+self._entry.winfo_x()+(self._padding[0]*2)+5,
                             y=self._entry.winfo_y()+5) 
        elif self._isCalendar:
            self._icon = Icon(self.canvas, 'assets/svg/calendar-icon.svg', output_height=self._entry.winfo_height()-10, output_width=self._entry.winfo_height()-10, command=self.__show_calendar)
            self._icon.place(x=self._entry.winfo_width()+self._entry.winfo_x()+(self._padding[0]*2)+5,
                             y=self._entry.winfo_y()+5) 

class Create_Calendar(Opk):
    def __init__(self, parent: Entry, canvas: tk.Canvas, font: ImageFont.truetype) -> None:
        super().__init__(canvas)
        self._week, self._month, self._day, self._time, self._year = [i for i in time.asctime().split(' ') if i]
        # self._month = 'Jan'

        self._weekend = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        self._monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 'July',  'August', 'September', 'October', 'November', 'December']

        self._calendar_canvas = tk.Canvas(self.canvas, background='white', highlightbackground=PRIMARY_COLOR, highlightthickness=1)
        self._body = tk.Canvas(self._calendar_canvas, background='white', highlightthickness=0, bd=0)
        self._font = font
        self._fontSize = self._font.getbbox('W')[3]
        self._parent = parent
        self.__isSet = False

        self._current_month = 0
        for month in range(len(self._monthNames)):
            if self._monthNames[month][:3] == self._month:
                self._current_month = month
        
        self._monthLabel = Label(self._calendar_canvas, text=self._monthNames[self._current_month], font=FONT(self._font.path, self._fontSize), background=self._calendar_canvas.cget('background'))
        self._yearLabel = Label(self._calendar_canvas, text=self._year, font=FONT(self._font.path, self._fontSize), background=self._calendar_canvas.cget('background'))

        self._upBtn = Icon(self._calendar_canvas, 'assets/svg/up-icon.svg', scale=1.5, command = lambda event: self.__moveMonth('up'))
        self._downBtn = Icon(self._calendar_canvas, 'assets/svg/down-icon.svg', scale=1.5, command = lambda event: self.__moveMonth('down'))

    def __monthDays(self, month):
        # print(month)
        year = int(self._yearLabel._text)
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            isLeapYear = True
        else:
            isLeapYear = False
        month_days = {
            'January': 31,
            'February': 28 if isLeapYear else 29,
            'March': 31,
            'April': 30,
            'May': 31,
            'June': 30,
            'July': 31,
            'August': 31,
            'September': 30,
            'October': 31,
            'November': 30,
            'December': 31,
        }
        return month_days[month]

    def __moveMonth(self, direction: Literal['up', 'down']):
        if self._current_month == (0 if direction == 'up' else 11):
            self._current_month = 12  if direction == 'up' else -1
        self._current_month += -1 if direction == 'up' else 1
        if self._current_month == (11 if direction == 'up' else 0):
            self._year = str(int(self._yearLabel._text)+(-1 if direction == 'up' else 1))
        self._yearLabel.change_text(text=self._year)
        self._monthLabel.change_text(text=self._monthNames[self._current_month])
        self._monthLabel.place(x=5, y=5)
        self._yearLabel.place(x=self._monthLabel._width+10, y=5)
        self._calendar_canvas.tag_raise(self.s.ID)
        self._body.delete('all')
        self.__generateDay(False)

    def __calculate_day_of_week(self, date_str):
        # Parse the date string into day, month, and year
        month, day, year = map(int, date_str.split('-'))

        # Get the last two digits of the year and the full year
        YY = year % 100

        # Calculate the Year Code
        year_code = (YY + (YY // 4)) % 7

        # Month Codes
        month_codes = {
            1: 0,  # January
            2: 3,  # February
            3: 3,  # March
            4: 6,  # April
            5: 1,  # May
            6: 4,  # June
            7: 6,  # July
            8: 2,  # August
            9: 5,  # September
            10: 0, # October
            11: 3, # November
            12: 5  # December
        }

        # Get the Month Code
        month_code = month_codes[month if month != 0 else 12]

        # Calculate the Century Code
        if year >= 1700 and year < 1800:
            century_code = 2
        elif year >= 1800 and year < 1900:
            century_code = 2
        elif year >= 1900 and year < 2000:
            century_code = 0
        elif year >= 2000 and year < 2100:
            century_code = 6
        elif year >= 2100 and year < 2200:
            century_code = 4
        elif year >= 2200 and year < 2300:
            century_code = 2
        elif year >= 2300 and year < 2400:
            century_code = 0
        else:
            raise ValueError("Year must be between 1700 and 2399.")

        # Determine if it's a leap year
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            leap_year_code = 1 if month == 1 or month == 2 else 0
        else:
            leap_year_code = 0

        # Calculate the day of the week using the formula
        total = (year_code + month_code + century_code + day - leap_year_code) % 7

        # Map the result to the corresponding weekday
        weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # return weekdays[total]
        return total

    def __generateDay(self, isStart = True):
        column = 0
        row = 0
        for week in self._weekend:
            temp = Label(self._body, week[:2], self._font)
            temp.place(rely=(1/8)*row, y=5, relx=(1/7)*column, x=self._fontSize-3, anchor='n')
            column += 1
        column = 0
        row += 1

        days = {}
        displayDay = self.__monthDays(self._monthNames[self._current_month-1]) - self.__calculate_day_of_week(f'{self._current_month}-{self.__monthDays(self._monthNames[self._current_month-1])}-{str(int(self._yearLabel._text)+(-1 if self._current_month == 0 else 0))}')
        isPrevMonth = True
        isCurrentMonth = False
        isNextMonth = False
        for day in range(7*6):
            days[day+1] = Button(self._body, str(displayDay), self._font, hover=False, radius=0, width=28, foreground='#aaa' if not isCurrentMonth else '#000')
            if self.__monthDays(self._monthNames[self._current_month]) > displayDay and isCurrentMonth:
                days[day+1].command = lambda event, day=day: self.__selectDay(days[day+1])
            elif self.__monthDays(self._monthNames[self._current_month-1]) > displayDay and isPrevMonth or isNextMonth:
                days[day+1].hand = ''
            else:
                if isCurrentMonth:
                    days[day+1].hand = 'hand2' 
                    days[day+1].command = lambda event, day=day: self.__selectDay(days[day+1])
                    isCurrentMonth = False
                    isNextMonth = True
                if not isNextMonth:
                    isCurrentMonth = True
                    days[day+1].hand = ''
                isPrevMonth = False
                displayDay = 0
            displayDay += 1
            days[day+1].place(rely=(1/8)*row, y=(row*3)+3, relx=(1/7)*column, x=self._fontSize-3, anchor='n')
            if (day+1) % 7 == 0:
                column = 0
                row += 1
            else:
                column += 1

        if isStart:
            self.__selectDay(days[int(self._day)+self.__calculate_day_of_week(f'{self._current_month}-{self.__monthDays(self._monthNames[self._current_month-1])}-{str(int(self._yearLabel._text)+(-1 if self._current_month == 0 else 0))}')+1])

    def __changeMonth(self):
        pass
        self.ID

    def place(self, y=0, x=0, rely: float = 0, relx: float = 0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw', width: int = None, height: int = None):
        self._calendar_canvas.place(y=y, x=x, rely=rely, relx=relx, anchor=anchor, height=self._fontSize+6, width=width)
        self._monthLabel.place(y=5, x=5)
        self._yearLabel.place(y=5, x=self._monthLabel._width+10)

        self._downBtn.place(relx=1, rely=0.5, anchor='e', x=-5)
        self._upBtn.place(relx=1, rely=0.5, anchor='e', x=-10-self._downBtn._rect.size[0])
        
        self.s = DrawLine(self._calendar_canvas)
        self.s.place(y=(self._fontSize)+4, padding=3)

        self._calendar_canvas.place(height=((self._fontSize+6)*8)+6)
        self._body.place(y=(self._fontSize)+5, x=1, relheight=1, relwidth=1, height=-((self._fontSize)+6), width=-2)
        self.__isSet = True
        self.__generateDay()

    def __selectDay(self, widget):
        try:
            if type(self._Selected_ID) == int:
                self._body.delete(self._Selected_ID)
        except:
            pass
        day = widget._text
        bbox = self._body.bbox(widget.ID)
        circumference = max(bbox[2]-bbox[0], bbox[3]-bbox[1]) - 2
        rect = Image.new('RGBA',
                         (circumference, circumference),
                         '#f000')
        draw = ImageDraw.Draw(rect)
        draw.rounded_rectangle((0,0,circumference-1, circumference-1), radius=circumference/2, fill=PRIMARY_COLOR)
        self._render = ImageTk.PhotoImage(rect)
        self._Selected_ID = self._body.create_image(bbox[0]+1, bbox[1]-((circumference-1)/4), anchor='nw', image=self._render)
        self._body.tag_lower(self._Selected_ID)
        self._parent._textVariable.set(f'{self._current_month+1 if int(self._current_month+1) > 9 else '0'+str(self._current_month+1)}-{day if int(day) > 9 else '0'+day}-{self._year}')
        if not self.__isSet:
            self.destroy()
        self.__isSet = False
        self._parent._entry.config(foreground='#000')

    def destroy(self):
        self._calendar_canvas.destroy()

class Button(Opk):
    def __init__(self, canvas: tk.Canvas, text: str, font: ImageFont.truetype, border: float = 0, width: int = 0, height: int = 0, 
                 foreground: str = ..., background: str = ..., outline: str = ..., radius: float = ..., padding: int = 0, 
                 angle: float = 0, command: callable = ..., *, corners: tuple[bool, bool, bool, bool] | None = None, hover: bool = True) -> None:
        super().__init__(canvas)
        # Text
        self._text = text
        self._font = font
        # Text Size
        self._left, self._top, self._right, self._bottom = self._font.getbbox(self._text)
        # Size
        self._border = border
        self._width = width if width > (self._right - self._left) else (self._right - self._left) 
        self._height = height if height > (self._bottom - self._top) else (self._bottom - self._top)
        self._padding = (padding+1)
        self._radius = radius
        self._angle = angle
        # Color
        self._foreground = foreground if foreground != ... else '#000'
        self._background = background if background != ... else '#fff0'
        self._outline = outline if outline != ... else '#000'
        # Boolean
        self._corners = corners
        self._canHover = hover
        self.__isPlaced = False
        # Command
        self.command = command if command != ... else 'No Command Set'
        self.hand = 'hand2'

        self._rect = Image.new('RGBA', (
                                self._width + (self._padding*2),
                                self._height + (self._padding*2)
                                ), '#0000')

    def change_text(self, text):
        bbox = self.canvas.bbox(self.ID)
        self._width = self._font.getbbox(text)[2] + self._padding[0]*2
        self._height = self._font.getbbox(text)[3] + self._padding[1]*2
        self.canvas.delete(self.ID)
        self._rect = Image.new('RGBA', (
                                self._width,
                                self._height
                                ), '#f000')
        self._text = text
        self.__create_text
        self._render = ImageTk.PhotoImage(self._rect)
        self.ID = self.canvas.create_image(bbox[0], bbox[1], anchor=self._anchor, image=self._render)

    def __create_text(self):
        draw = ImageDraw.Draw(self._rect)
        draw.text(((self._padding+(self._width/2))-(self._right/2), 
                   (-self._top+self._padding+(self._height/2))-((self._bottom-self._top)/2)), 
                  text=self._text, 
                  fill=self._foreground if self._foreground != ... else '#0000', 
                  font=self._font)

    def __create_background(self):
        draw = ImageDraw.Draw(self._rect)
        draw.rounded_rectangle((0,0,self._width+(self._padding*2)-1, self._height+(self._padding*2)-1), 
                               radius=(self._height+(self._padding*2))/2 if self._radius == ... else min(self._radius, (self._height+(self._padding*2))-2), 
                               fill = '#0000'  if self._background == ... else self._background, 
                               outline ='#000' if self._outline == ... else self._outline,
                               width = self._border,
                               corners=self._corners)

    def __display(self):
        self._rect = Image.new('RGBA', (
                                self._width + (self._padding*2),
                                self._height + (self._padding*2)
                                ), '#0000')
        self.__create_background() 
        self.__create_text()
        self._rect_r = self._rect.rotate(self._angle, expand=True)
        self._render = ImageTk.PhotoImage(self._rect_r)

    def place(self, y=0, x=0, rely: float=0, relx: float=0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw'):
        self.__display()

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx),
                                           y+(self.canvas.winfo_height()*rely), anchor=anchor, image=self._render)

        if not self.__isPlaced:
            self.canvas.tag_bind(self.ID, '<Button-1>', self.command)
            self.canvas.tag_bind(self.ID, '<Enter>', self.onhover)
            self.canvas.tag_bind(self.ID, '<Leave>', self.onLeave)
            self.__canvas_width = self.canvas.winfo_width()
            self.__canvas_height = self.canvas.winfo_height()
            self.__original_pos = [y, x, rely, relx, anchor]
            self.canvas.bind('<Configure>', self.dynamicChange)
        else:
            self.__isPlaced = True  

    def dynamicChange(self, event):
        if event.width != self.__canvas_width or event.height != self.__canvas_height:
            self.place(y=self.__original_pos[0], x=self.__original_pos[1], rely=self.__original_pos[2], relx=self.__original_pos[3], anchor=self.__original_pos[4])
        self.__canvas_width = event.width
        self.__canvas_height = event.height

    def onhover(self, event, expand = 10):
        event.widget.config(cursor=self.hand)
        if not self._canHover:
            return 0

        self._width += expand
        self._height += int(expand/4)

        self.__display()
        self.canvas.update()

        self.canvas.itemconfig(self.ID, image=self._render)
        if self._angle < 90 and self._angle > -90:
            self.canvas.move(self.ID, expand/2, 0)
        else:
            self.canvas.move(self.ID, 0, -int(expand/4))

        self._width -= expand
        self._height -= int(expand/4)

    def onLeave(self, event, expand = 10):
        event.widget.config(cursor='')
        if not self._canHover:
            return 0

        self.__display()

        self.canvas.itemconfig(self.ID, image=self._render)
        old_coords = self.canvas.coords(self.ID)
        if self._angle < 90 and self._angle > -90:
            self.canvas.move(self.ID, -expand/2, 0)
        else:
            self.canvas.move(self.ID, 0, int(expand/4))

class DropDown(Opk):
    def __init__(self, canvas: tk.Canvas, text: str, font: ImageFont.truetype, foreground: str = ..., background: str = ..., style: Literal['box', 'circle'] = 'box') -> None:
        super().__init__(canvas)
        padding = 10

        self.size = font.getbbox(text)
        self.height = self.size[3]-self.size[1]+padding
        self.width = self.size[2]+padding

        image = Image.new("RGBA", (self.canvas.winfo_width(), self.canvas.winfo_height()), '#0000' if background == ... else background)
        draw = ImageDraw.Draw(image)
        draw.text((font.getbbox('>')[2]+5, -self.size[1]), text, font=font, fill= foreground if foreground != ... else '#000')
        draw.text((2, -self.size[1]+(self.size[3]/2)), '>', font=font, fill= foreground if foreground != ... else '#000')
        draw.line((font.getbbox('>')[2]+3, (self.size[3]-self.size[1]/2), 200, (self.size[3]-self.size[1]/2)), width=1, fill= foreground if foreground != ... else '#000')

        dropCollision = Image.new('RGBA', (200, font.getbbox('>')[1]), '#f000')

        self.photo_image = ImageTk.PhotoImage(image)
        self.collision_image = ImageTk.PhotoImage(dropCollision)

    def place(self, y=0, x=0):
        super().place(y, x)
        y += -self.size[1]+(self.size[3])-1
        self.COLLISION_ID = self.canvas.create_image((self.canvas.winfo_width()/2) - (self.width/2) if x == 0 else x, y, anchor=tk.NW, image=self.collision_image)

class DrawLine(Opk):
    def __init__(self, canvas: tk.Canvas, fill: str = ..., width: int = ..., weight: int = ..., orientation: Literal['horizontal', 'vertical'] = 'horizontal') -> None:
        super().__init__(canvas)
        self._fill = fill if fill != ... else '#959595'
        self._weight = weight if weight != ... else 1
        self._orientation = orientation
        self._width = width if width != ... else (self.canvas.winfo_width() if self._orientation == 'horizontal' else self.canvas.winfo_height())

    def __draw_line(self, padding):
        padding *= 2
        self._rect = Image.new('RGBA',
                               (self._width-padding, self._weight) if self._orientation == 'horizontal' else (self._weight, self._width-padding),
                               self._fill)

    def place(self, y=0, x=0, rely: float = 0, relx: float = 0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw', padding:int=1):
        self.__draw_line(padding)
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx)+(padding if self._orientation == 'horizontal' else 0),
                                           y+(self.canvas.winfo_height()*rely)+(padding if self._orientation == 'vertical' else 0), anchor=anchor, image=self._render)

class Table(Opk):
    def __init__(self, canvas: tk.Canvas, header: dict, font: ImageFont.truetype, padding: int | tuple[int, int] = 5, height: int = ...) -> None:
        '''Header = {Text: Width}'''
        super().__init__(canvas)

        self._font = font
        self._font_rect = font.getbbox('W')
        if type(padding) == tuple:
            self._padding = padding
        else:
            self._padding = [padding, padding]
        self._header = header
        self._height = height if height != ... else 480

        self._current_row = -1
        self._row = []
        
        self._rect = Image.new('RGBA', 
                               (self.canvas.winfo_width(),
                                self._font_rect[3]-self._font_rect[1]+(self._padding[1]*2)), 
                               SECONDARY_COLOR)
        self.__create_header()
        self.__create_table()
        
    def __create_header(self):
        draw = ImageDraw.Draw(self._rect)
        temp = 0
        for x in self._header:
            font_rect = self._font.getbbox(x)
            draw.text((
                self._padding[0]+temp, 
                self._padding[1]-font_rect[1]
            ), text=x, fill='#000', font=self._font)
            temp += self._header[x] if self._header[x] > font_rect[2]-font_rect[0] else font_rect[2]-font_rect[0]+(self._padding[0]*2)
        self._render = ImageTk.PhotoImage(self._rect)
        self.ID = self.canvas.create_image(0, 0, anchor='se', image=self._render)

    def create_row(self, background: str= ..., height: int = 150):
        self._current_row += 1
        self._canvas.update()
        canvas = tk.Canvas(self._canvas, width=self._canvas.winfo_width(), height=height)
        if background != ...:
            canvas.configure(background=background)
        canvas.create_line(0, height-1, self._canvas.winfo_width()-1, height-1, fill='gray75')
        result = {'ID': self._canvas.create_window(0, (height * self._current_row) + 1, anchor='nw', window=canvas),
                  'canvas': canvas}

        self._canvas.configure(scrollregion=self._canvas.bbox('all'))
        self._row.append(result)
        return result

    def on_scroll(self, event):
        # Event.delta is typically 120 for scroll up and -120 for scroll down
        if event.delta > 0:
            self._canvas.yview_scroll(-1, "units")  # Scroll up
        elif event.delta < 0:
            self._canvas.yview_scroll(1, "units")   # Scroll down

    def __create_table(self):
        self._frame = tk.Frame(self.canvas,
                          width=self.canvas.winfo_width(), 
                          height=self._height, bd=0, highlightthickness=0)
        self._frame.place(y=self._rect.size[1], anchor='se')
        
        self._canvas = tk.Canvas(self._frame, bd=0, highlightthickness=0, height=self._height)
        self._canvas.place(x=0, y=0, relheight=1, relwidth=1)

        self._canvas.bind_all('<MouseWheel>', self.on_scroll)


    def place(self, y=0, x=0,rely:float=0,relx:float=0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw', padding: int= 10):
        self._rect = Image.new('RGBA', 
                               (self.canvas.winfo_width()-(padding*2),
                                self._font_rect[3]-self._font_rect[1]+(self._padding[1]*2)), 
                               SECONDARY_COLOR)
        self.__create_header()

        self.canvas.itemconfigure(self.ID, image=self._render, anchor='nw')
        self.canvas.move(self.ID, x+padding, y)

        self._frame.update()
        self._frame.configure(width=self._frame.winfo_width()-(padding*2))
        self._frame.place(x=x+padding, y=y+self._rect.size[1], relx=relx, rely=rely, anchor='nw')



if __name__ == '__main__':
    window = tk.Tk()

    window.geometry('800x500')
    # window.resizable(False, False)

    canvas = tk.Canvas(window, bd=0, highlightthickness=0)
    canvas.pack(fill='both', expand=True)


    # b = Label(canvas, text='ACSS CITE', font=FONT(Lobster, 40), foreground=PRIMARY_COLOR, border=1, radius=10)
    # b.place(y=50)
    # b1 = Label(canvas, text='ACSS CITE', font=FONT(Lobster, 40), foreground=PRIMARY_COLOR, border=1, radius=10)
    # b1.place(y=100)
    # b1 = Button(canvas, text='MEMBERS', font=FONT(OpenSans, 24), foreground=PRIMARY_COLOR, outline=PRIMARY_COLOR, 
    #             width=150, border=1, radius=8)
    # b1.place(y=150, anchor='e')
    b2 = Button(canvas, text='MEMBERS', font=FONT(OpenSans, 24), foreground=PRIMARY_COLOR, outline=PRIMARY_COLOR, 
                width=150, border=1, angle=0,
                corners=[True, True, False, False])
    b2.place(y=250, anchor='w')

    svg = Icon(canvas, 'assets/svg/add-entry-icon.svg')
    svg.place()

    tbl = Table(canvas, {'No.': 50, 'Personal Information': 0}, font=FONT(FuturaHeavy, 18), padding=(10, 5))
    # for i in range(20):
    #     temp_row = tbl.create_row()
    #     temp_row['canvas']
    #     t = Label(temp_row['canvas'], i+1, font=FONT(FuturaBook, 18), foreground='#000')
    #     t.place(x=15, rely=0.5, anchor='w')
    #     # print(temp_row)
    # tbl.place(y=10)

    # entry = Entry(canvas, outline=PRIMARY_COLOR, foreground=PRIMARY_COLOR, border=1, displayText='Search')
    # entry.place(x=100, y=100)
    # entry1 = Entry(canvas, outline=PRIMARY_COLOR, foreground=PRIMARY_COLOR, border=1, displayText='Search')

    # line = DrawLine(canvas, orientation='vertical', width=100)
    # line.place(y=0, relx=1, x=-10)


    # entry1.place(x=100, y=200)

    ageVar = tk.IntVar()

    age = Entry(canvas, 
                        font=FONT(FuturaBook, 16), 
                        width=3, 
                        textVariable=ageVar, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        variableLimit=150)
    age.place(x=60, y=60)
    dob  = Entry(canvas, 
                        font=FONT(FuturaBook, 20), 
                        width=12, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='MM-DD-YYYY', isCalendar=True)
    dob.place(x=80, y=100)
    # b2 = DropDown(canvas, text='SPORTS', font=FONT(OpenSans, 18), 
    #             #   background='blue'
    #               )
    # b2.place(y=150, x=100)
    # b3 = DropDown(canvas, text='DANCE', font=FONT(OpenSans, 18), 
    #             #   background='red'
    #               )
    # b3.place(y=200, x=100)

    # t = Table(canvas, font=FONT(OpenSans, 24))
    # t.place()

    window.mainloop()

    print('-- [ Program End ] --')