from PIL import ImageFont

Lobster = 'assets/font/Lobster-Regular.ttf'
OpenSans = 'assets/font/OpenSans-VariableFont_wdth,wght.ttf'
FuturaBook = 'assets/font/futura/Futura Book font.ttf'
FuturaHeavy = 'assets/font/futura/Futura Heavy font.ttf'

FONT = lambda font, size: ImageFont.truetype(font, size)

PRIMARY_COLOR = '#716EF4'
SECONDARY_COLOR = '#F2F46E'
SUCCES_COLOR = '#91F46E'
ERROR_COLOR = '#F46E6E'

WIDTH = 1280
HEIGHT = 768
WIN_POS_X = (WIDTH / 2)
WIN_POS_Y = (HEIGHT / 2)