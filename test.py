'''
    What's Wrong with this code cause every time I remove/comment line 81 the text won't show up?
'''
import tkinter as tk
import tkinter.ttk as ttk

from PIL import Image, ImageTk, ImageDraw, ImageFont
import cairosvg
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
    def __init__(self, canvas: tk.Canvas, text: str, font: ImageFont.truetype, border: float = 0, width: int = 0, height: int = 0, foreground: str = ..., background: str = ..., outline: str = ..., radius: float = 0, padding = 0) -> None:
        super().__init__(canvas)
        # Text
        self._text = str(text)
        self._font = font
        # Text Size
        self._left, self._top, self._right, self._bottom = self._font.getbbox(self._text)
        # Size
        self._border = border
        self._width = width if width > (self._right - self._left) else (self._right - self._left) 
        self._height = height if height > (self._bottom - self._top) else (self._bottom - self._top)
        self._padding = padding
        self._radius = radius
        # Color
        self._foreground = foreground if foreground != ... else '#000'
        self._background = background
        self._outline = outline if outline != ... else '#000'
        # Boolean
        self.__isPlaced = False  
        
        self._rect = Image.new('RGBA', (
                                self._width + (self._padding*2),
                                self._height + (self._padding*2)
                                ), '#0000')

    def change_text(self, text):
        bbox = self.canvas.bbox(self.ID)
        self.canvas.delete(self.ID)
        self._rect = Image.new('RGBA',
                               self._rect.size,
                               '#0000')
        self._text = text
        self.__create_text
        self._render = ImageTk.PhotoImage(self._rect)
        print(bbox)
        self.ID = self.canvas.create_image(bbox[0], bbox[1], anchor=self._anchor, image=self._render)

    def __create_text(self):
        draw = ImageDraw.Draw(self._rect)
        draw.text((self._padding, -self._top+self._padding), text=self._text, fill=self._foreground if self._foreground != ... else '#0000', font=self._font)

    def __create_background(self):
        draw = ImageDraw.Draw(self._rect)
        draw.rounded_rectangle((0,0,self._width+(self._padding*2)-1, self._height+(self._padding*2)-1), 
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
        if not self.__isPlaced:
            self.canvas.bind('<Configure>', self.dynamicChange)
            pass
        else:
            self.__isPlaced = True  
            
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
    def __init__(self, canvas: tk.Canvas, displayText = ..., font: tuple[str, int] = (FuturaBook, 24), 
                 width: int = 20, height: int = 0, foreground: str = ..., background: str = ..., 
                 outline: str = ..., padding: int | tuple[int, int] = 0, border: int=1, radius: int=...,
                 textVariable: tk.Variable = ..., variableLimit: int = ..., isCalendar: bool = ...) -> None:
        super().__init__(canvas)
        #~ Boolean
        self._isCalendar = isCalendar if isCalendar != ... else False
        self._showCalendar = False
        #~ Text
        self._displayText = (displayText if displayText != ... else '') if textVariable == ... else textVariable.get()
        self._font = (FONT(font[0], font[1]), font[1])
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
                               font=self._font, textvariable=self._textVariable)
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

        self.months = {
            'January': 1,
            'February': 2,
            'March': 3,
            'April': 4,
            'May': 5,
            'June': 6,
            'July': 7, 
            'August': 8,
            'September': 9,
            'October': 10,
            'November': 11,
            'December': 12,
        }

        self._calendar_canvas = tk.Canvas(self.canvas, background='white', highlightbackground=PRIMARY_COLOR, highlightthickness=1)
        self._font = font
        self._parent = parent

        self._month = Label(self._calendar_canvas, 'July', font=self._font)
        self._year = Label(self._calendar_canvas, '2024', font=self._font)

        self._upBtn = Icon(self._calendar_canvas, 'assets/svg/up-icon.svg', scale=1.5, command=self.__prevMonth)
        self._downBtn = Icon(self._calendar_canvas, 'assets/svg/down-icon.svg', scale=1.5, command=self.__nextMonth)

    def __prevMonth(self, event):
        self._month.change_text('Test')
        pass

    def __nextMonth(self, event):
        pass

    def place(self, y=0, x=0, rely: float = 0, relx: float = 0, anchor: Literal['center', 'n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] = 'nw', width: int = None, height: int = None):
        self._calendar_canvas.place(y=y, x=x, rely=rely, relx=relx, anchor=anchor, height=0, width=width)
        self._month.place(x=5, y=5)
        self._year.place(x=self._month._width+10, y=5)

        self._downBtn.place(relx=1, rely=0.5, y=self._upBtn._rect.size[1], anchor='ne', x=-5)
        self._upBtn.place(relx=1, rely=0.5, y=self._downBtn._rect.size[1], anchor='ne', x=-10-self._downBtn._rect.size[0])
        
        self.s = DrawLine(self._calendar_canvas)
        self.s.place(y=self._font.getbbox('W')[3]+5, padding=3)

        row = 1
        column = 0
        days = {}
        for day in ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']:
            temp = Label(
                self._calendar_canvas,
                text=day,
                font=FONT(FuturaBook, self._font.getbbox('W')[3] - 3),
                # background='red' if day%2 == 0 else 'blue', # For Debugging
                radius=0,
            )
            temp.place(
                y=((self._font.getbbox('W')[3] + 6) * row) + 5,
                x=((self._calendar_canvas.winfo_width() / 7) * column) + 5
            )
            column += 1
        column = 0
        row += 1

        for day in range(31):
            day_value = day + 1
            days[day] = Button(
                self._calendar_canvas,
                text=str(day_value) if day_value > 9 else f'  {day_value}',
                font=FONT(FuturaBook, self._font.getbbox('W')[3] - 3),
                hover=False,
                # background='red' if day%2 == 0 else 'blue', # For Debugging
                radius=0,
                command=lambda event, day=day_value, widget=days: self.__DayClick(days[day-1], day)
            )
            days[day].place(
                y=((self._font.getbbox('W')[3] + 6) * row)+5,
                x=((self._calendar_canvas.winfo_width() / 7) * column)+5
            )
            column += 1
            if day_value % 7 == 0:
                column = 0
                row += 1
        self._calendar_canvas.place(height=((self._font.getbbox('W')[3]+6)*(row+1))+6)

    def __DayClick(self, widget, day):
        try:
            if type(self._Selected_ID) == int:
                self._calendar_canvas.delete(self._Selected_ID)
                print('Deleted')
        except:
            pass
        print(day)
        font = FONT(FuturaBook, self._font.getbbox('W')[3]-3)
        bbox = self._calendar_canvas.bbox(widget.ID)
        circumference = max(bbox[2]-bbox[0], bbox[3]-bbox[1]) + 10
        rect = Image.new('RGBA',
                         (circumference, circumference),
                         '#f000')
        draw = ImageDraw.Draw(rect)
        draw.rounded_rectangle((0,0,circumference-1, circumference-1), radius=circumference/2, fill=PRIMARY_COLOR)
        draw.text((6,5), ('' if day > 9 else '  ')+str(day), fill='#000', font=font)
        self._render = ImageTk.PhotoImage(rect)
        self._Selected_ID = self._calendar_canvas.create_image((bbox[0])-((circumference-(bbox[2]-bbox[0]))/2), 
                                                               (bbox[1])-((circumference-(bbox[3]-bbox[1]))/2), anchor='nw', image=self._render)
        self._parent._textVariable.set(f'{str(self.months[self._month._text]) if self.months[self._month._text] > 9 else '0'+str(self.months[self._month._text])}-{str(day) if day > 9 else '0'+str(day)}-{self._year._text}')
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
        self._background = background if background != ... else '#fff'
        self._outline = outline if outline != ... else '#000'
        # Boolean
        self._corners = corners
        self._canHover = hover
        self.__isPlaced = False
        # Command
        self.command = command if command != ... else 'No Command Set'

        self._rect = Image.new('RGBA', (
                                self._width + (self._padding*2),
                                self._height + (self._padding*2)
                                ), '#0000')

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
        event.widget.config(cursor='hand2')
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

if __name__ == '__main__':
    window = tk.Tk()

    window.geometry('800x500')

    canvas = tk.Canvas(window, bd=0, highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    dob  = Entry(canvas, 
                        font=(FuturaBook, 20), 
                        width=12, 
                        outline=PRIMARY_COLOR, 
                        radius=5, 
                        displayText='MM-DD-YYYY', isCalendar=True)
    dob.place(x=80, y=100)

    window.mainloop()

    print('-- [ Program End ] --')