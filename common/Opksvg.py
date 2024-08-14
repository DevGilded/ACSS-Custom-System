import os
import cairosvg
from typing import Any

tempOutput = []

def ToPNG(file_path: str, scale: int = 1, output_height: Any | None = None, output_width: Any | None = None) -> str:
    global tempOutput
    try:
        imgName = file_path.split('/')[-1].split('.')
        print(imgName)
        imgName = f'assets\\temp\\image\\{imgName[0]}.png'
    except:
        pass

    cairosvg.svg2png(url=file_path, write_to=imgName, scale=scale, output_height=output_height, output_width=output_width)
    tempOutput.append(imgName)
    return imgName

def clear() -> None:
    try:
        exception_file = ''
        for tempPath in tempOutput:
            exception_file = tempPath
            os.remove(tempPath)
            print(f'File {tempOutput} deleted successfully.')
    except FileNotFoundError:
        print(f'File {exception_file} does not exist.')
    except PermissionError:
        print(f'Permission denied: Unable to delete {exception_file}.')
    except Exception as e:
        print(f'An error occurred: {e}')