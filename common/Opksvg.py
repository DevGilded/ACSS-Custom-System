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
    exception_file = ''
    try:
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
    finally:
        # Making sure deleting all file inside the temp image path if there's something or someone put a file in it.
        for path in os.scandir('assets/temp/image'):
            os.remove(path.path)
            print(f'File {path.path} deleted successfully.')