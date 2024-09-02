from PIL import ImageFont

Lobster = 'assets/font/Lobster-Regular.ttf'
OpenSans = 'assets/font/OpenSans-VariableFont_wdth,wght.ttf'
FuturaBook = 'assets/font/futura/Futura Book font.ttf'
FuturaHeavy = 'assets/font/futura/Futura Heavy font.ttf'

FONTLIST = {
    'Futura Bk BT': 'assets/font/futura/Futura Book font.ttf',
    'Futura Hv BT': 'assets/font/futura/Futura Heavy font.ttf',
}

# def FONT(font, size) -> ImageFont.truetype:
#     return ImageFont.truetype(font, size)

FONT = lambda font, size: ImageFont.truetype(font, size)
TkinterFontModifiyer = 1.318

PRIMARY_COLOR = '#716EF4'
SECONDARY_COLOR = '#F2F46E'
SUCCES_COLOR = '#91F46E'
ERROR_COLOR = '#F46E6E'
BLANK = '#ffffff'

WIDTH = 1280
HEIGHT = 768