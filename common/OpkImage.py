import string

from functools import lru_cache

from PIL import Image, ImageFont, ImageDraw
from typing import Literal

@lru_cache
def image_text(text: str, font: ImageFont.FreeTypeFont):
    _, _, width, height = font.getbbox(text)
    _, _, _, h = font.getbbox(string.ascii_uppercase+string.ascii_lowercase)
    _, _, w, _ = font.getbbox('A')

    img = Image.new('RGBA', (width+w, h), '#FFF0')
    
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text=text, font=font, fill='#000')

    return img

def combine_two_image(image1: Image.Image, image2: Image.Image, orientation: Literal['horizontal', 'vertical'] = 'vertical'):

    width1, height1 = image1.size
    width2, height2 = image2.size

    match orientation:
        case 'vertical':
            combine_width = max(width1, width2)
            combine_height = height1 + height2
        case 'horizontal':
            combine_width = width1 + width2
            combine_height = max(height1, height2)
    
    img = Image.new('RGBA', (combine_width, combine_height), '#FFF0')

    img.paste(image1, (0, 0))
    img.paste(image2, (0 if orientation == 'vertical' else width1, 0 if orientation == 'horizontal' else height1,))

    return img

@lru_cache
def create_circle(radius = 4, background = 'white', outline = 'black', width = 1) -> Image:
    PI = 3.14159
    circumference = 2 * PI * radius
    resolution = 5
    circumference *= resolution

    img = Image.new('RGBA', (int(circumference), int(circumference)), '#0000')

    draw = ImageDraw.Draw(img)
    draw.ellipse((0, 0, circumference-1, circumference-1), fill = background, outline = outline, width = width * resolution)

    # img.show()
    circumference //= resolution
    return img.resize((int(circumference), int(circumference)))

if __name__ == '__main__':
    print(create_circle())
    create_circle(10).show()