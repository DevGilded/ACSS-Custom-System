import tkinter as tk

from PIL import Image, ImageTk, ImageDraw, ImageFont
import cairosvg, os
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
        self._text = text
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
        self._foreground = foreground
        self._background = background
        self._outline = outline
        
        self._rect = Image.new('RGBA', (
                                self._width + (self._padding*2),
                                self._height + (self._padding*2)
                                ), '#0000')
        

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

    def place(self, y=0, x=0,rely:float=0,relx:float=0):
        self.__create_background()
        self.__create_text()
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx), y+(self.canvas.winfo_height()*rely), anchor=tk.NW, image=self._render)

class Icon(Opk):
    def __init__(self, canvas: tk.Canvas, image: str, scale:int=1) -> None:
        super().__init__(canvas)
        if image.split('.')[-1] == 'svg':
            try:
                self._image_name = image.split('/')[-1].split('.')
            except:
                pass

            cairosvg.svg2png(url=image, write_to=f'assets/svg_to_png/{self._image_name[0]}.png', scale=scale)
            self._image_path = f'assets/svg_to_png/{self._image_name[0]}.png'
        else:
            self._image_path = image

        self._rect = Image.open(self._image_path)

    def place(self, y=0, x=0,rely:float=0,relx:float=0):
        self._render = ImageTk.PhotoImage(self._rect)

        self.ID = self.canvas.create_image(x+(self.canvas.winfo_width()*relx), y+(self.canvas.winfo_height()*rely), anchor=tk.NW, image=self._render)

class Entry(Opk):
    def __init__(self, canvas: tk.Canvas, displayText: str = '', font: ImageFont.truetype = ..., width: int = 20, height: int = 0) -> None:
        super().__init__(canvas)
        # Text
        self._displayText = displayText
        self._font = FONT(FuturaBook, 12) if font == ... else font
        # Size
        self._width = width
        self._height = height

    def __create_entry(self):
        self._entry = tk.Entry(canvas, relief='flat', width=self._width)

    # def __create_back

    def place(self, y=0, x=0, rely: float = 0, relx: float = 0):
        self.__create_entry()

        self._entry.place(y=y, x=x)

class Button(Opk):
    def __init__(self, canvas: tk.Canvas, text: str, font: ImageFont.truetype, border: float = 0, width: int = 0, height: int = 0, foreground: str = ..., background: str = ..., outline: str = ..., radius: float = 0, padding: int = 0, angle: float = 0, command: callable = ..., *, corners: tuple[bool, bool, bool, bool] | None = None) -> None:
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
        self._padding = (padding + 10)
        self._radius = radius
        self._angle = angle
        # Color
        self._foreground = foreground
        self._background = background
        self._outline = outline
        # Boolean
        self._corners = corners
        # Command
        self.command = command if command != ... else lambda event: print('[ NO COMMAND SET ]')

    def __create_text(self):
        draw = ImageDraw.Draw(self._rect)
        draw.text(((self._padding+(self._width/2))-(self._right/2), (-self._top+self._padding+(self._height/2))-((self._bottom-self._top)/2)), text=self._text, fill=self._foreground if self._foreground != ... else '#0000', font=self._font)

    def __create_background(self):
        draw = ImageDraw.Draw(self._rect)
        draw.rounded_rectangle((0,0,self._width+(self._padding*2)-1, self._height+(self._padding*2)-1), 
                               radius = min(self._radius, min(self._width+(self._padding*2)-1, self._height+(self._padding*2)-1))-1, 
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

    def place(self, y=..., x=..., rely: float=0, relx: float=0):
        self.__display()

        self.ID = self.canvas.create_image(((self.canvas.winfo_width()/2) - (self._width/2) if x == ... else x)+(self.canvas.winfo_width()*relx), 
                                           (0 if y == ... else y)+(self.canvas.winfo_height()*rely), anchor=tk.NW, image=self._render)
        self.canvas.tag_bind(self.ID, '<Button-1>', self.command)
        self.canvas.tag_bind(self.ID, '<Enter>', self.onhover)
        self.canvas.tag_bind(self.ID, '<Leave>', self.onLeave)
    
    def onhover(self, event, expand = 20):
        self._width += expand
        self._height += int(expand/4)


        self.__display()

        self.canvas.itemconfig(self.ID, image=self._render)
        old_coords = self.canvas.coords(self.ID)
        if self._angle < 90 and self._angle > -90:
            self.canvas.coords(self.ID, old_coords[0]-int(expand/2), old_coords[1]-int(int(expand/4)/2))
        else:
            self.canvas.coords(self.ID, old_coords[0], old_coords[1]-int(expand/4))

        self._width -= expand
        self._height -= int(expand/4)

    def onLeave(self, event, expand = 20):
        self.__display()

        self.canvas.itemconfig(self.ID, image=self._render)
        old_coords = self.canvas.coords(self.ID)
        if self._angle < 90 and self._angle > -90:
            self.canvas.coords(self.ID, old_coords[0]+int(expand/2), old_coords[1]+int(int(expand/4)/2))
        else:
            self.canvas.coords(self.ID, old_coords[0], old_coords[1]+int(expand/4))

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

class Table(Opk):
    def __init__(self, canvas: tk.Canvas, font: ImageFont.truetype, header: list = ...) -> None:
        super().__init__(canvas)
        self.width = 100

        image = Image.new('RGBA', (100, 100), '#00f0')
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((0,0, 99, 99), outline='#000', fill='#0000', radius=10)

        self.photo_image = ImageTk.PhotoImage(image)

    def place(self, y=0, x=0):
        return super().place(y, x)

if __name__ == '__main__':
    window = tk.Tk()

    window.geometry('800x500')
    window.resizable(False, False)

    canvas = tk.Canvas(window, bd=0, highlightthickness=0)
    canvas.pack(fill='both', expand=True)

    b = Label(canvas, text='ACSS CITE', font=FONT(Lobster, 40), foreground=PRIMARY_COLOR, border=1, radius=10)
    b.place(y=50)
    b1 = Button(canvas, text='MEMBERS', font=FONT(OpenSans, 24), foreground=PRIMARY_COLOR, outline=PRIMARY_COLOR, 
                width=150, border=1, radius=8, angle=-90)
    b1.place(y=100)

    svg = Icon(canvas, 'assets/svg/add-entry-icon.svg')
    svg.place()

    entry = Entry(canvas)
    entry.place()
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