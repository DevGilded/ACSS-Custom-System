import os
import cairosvg
from typing import Any

tempOutput = []

def ToPNG(file_path: str, scale: float = 1, output_height: Any | None = None, output_width: Any | None = None) -> str:
    global tempOutput
    try:
        img_name = file_path.split('/')[-1].split('.')
        # print(file_path)
        # print(img_name)
        img_name = f'assets\\temp\\image\\{img_name[0]}.png'
    except:
        pass

    cairosvg.svg2png(url=file_path, write_to=img_name, scale=scale, output_height=output_height, output_width=output_width)
    tempOutput.append(img_name)
    return img_name

def clear() -> None:
    try:
        exception_file = ''
        for tempPath in tempOutput:
            exception_file = tempPath
            os.remove(tempPath)
            print(f'File {tempPath} deleted successfully.')
    except FileNotFoundError:
        print(f'File {exception_file} does not exist.')
    except PermissionError:
        print(f'Permission denied: Unable to delete {exception_file}.')
    except Exception as e:
        print(f'An error occurred: {e}')