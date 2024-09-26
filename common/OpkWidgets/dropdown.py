import tkinter as tk
from typing import Literal, Union

class DropDown(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, text: str = '', values: list[Union[str, tk.Widget, dict]] = None, font = None, value_type: Literal['list', 'check', 'button'] = 'list', **kwargs):
        super().__init__(master, **kwargs)

        self._text = text
        self._font = ('Futura Bk Bt', 12) if font is None else font
        self._values = []
        if values:
            self._values.extend(values)
        self._type = value_type

        self.label = tk.Label(self, text=f'> {self._text}', font=self._font, **kwargs)
        self.label.pack(anchor=tk.NW)

        self.label.bind('<Button-1>', self.drop_value)

        self._widgets: list[tk.Widget] = []
        for value in self._values:
            if isinstance(value, tk.Widget):
                match type(value):
                    case tk.Button:
                        widget = tk.Button(self, font = self._font, **kwargs)
                        copy_widget(value, widget)
                    case tk.Label:
                        widget = tk.Label(self, font = self._font)
                        copy_widget(value, widget)
                    case tk.Frame:
                        widget = tk.Frame(self)
                        copy_widget(value, widget)
                    case _:
                        continue
            elif type(value) is dict:
                parameters = {'text': self._text, 'values': self._values, 'font': self._font, 'value_type': self._type}
                for param, val in parameters.items():
                    if param not in value:
                        value[param] = val

                value.update(kwargs)

                widget = DropDown(self, **value)
            else:
                # Create a new Label for the string value
                match self._type:
                    case 'list':
                        widget = tk.Label(self, text=value, font=self._font, justify=tk.LEFT, **kwargs)
                    case 'check':
                        background = kwargs.get('background', False)
                        widget = tk.Checkbutton(self, text=value, font=self._font, relief='flat', justify=tk.LEFT, name=value.lower(), **kwargs)
                        if background:
                            widget.configure(activebackground=background, selectcolor=background)
                    case 'button':
                        widget = tk.Button(self, text=value, font=self._font, justify=tk.LEFT, **kwargs)
                    case _:
                        raise Exception ('Invalid Typing')

            self._widgets.append(widget)

        # Initially hide all widgets
        self._hide_widgets()

    def drop_value(self, event: tk.Event):
        if self.label.cget('text').startswith('∨'):
            # Hide widgets
            self._hide_widgets()
            self.label.configure(text=f'> {self._text}')
        else:
            # Show widgets
            self._show_widgets()
            self.label.configure(text=f'∨ {self._text}')

    def _show_widgets(self):
        for widget in self._widgets:
            widget.pack(anchor=tk.NW, padx=5, pady=2)

    def _hide_widgets(self):
        for widget in self._widgets:
            widget.pack_forget()


def copy_widget(copy: tk.Widget, paste: tk.Widget) -> None:
    attributes = [
        'bg', 'fg', 'font', 'padx', 'pady', 'width', 'height',
        'borderwidth', 'relief', 'highlightbackground', 'highlightcolor',
        'highlightthickness', 'text', 'image', 'compound'
    ]

    for attr in attributes:
        try:
            value = copy.cget(attr)
            paste.configure(**{attr: value})
        except tk.TclError:
            pass


if __name__ == '__main__':
    window = tk.Tk()

    DD = DropDown(window, 'Saying',
                  ['Hello', 'World!',
                   'I\'m Mj Maruel L. Namok',
                   tk.Button(text='CLICK ME!'),
                   {'text': 'Other', 'values': ['Yes', 'NO'], 'value_type': 'list'}],
                  value_type='check')
    DD.pack()

    tk.Label(window, text='TEST').pack()

    print(type(DD))

    window.mainloop()