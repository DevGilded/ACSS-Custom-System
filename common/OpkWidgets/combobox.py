import tkinter as tk

from common.OpkWidgets.button import Button
from common.OpkWidgets.dropdown import DropDown
from settings import SECONDARY_COLOR

class ComboBox(tk.Frame):
    def __init__(self, master: tk.Misc | None = None, text: str = '', font = ('Futura Hv BT', 12), *_, values: list = None, show_selected: bool = False, combo_param: dict = None, box_param: dict = None, **kwargs):
        super().__init__(master, **kwargs)

        self._font = font
        self._show_selected = show_selected
        self._selected = None
        self._box = None
        self._values = ['all']
        if values:
            self._values.extend(values)
        self._checkboxes = []
        self._checkVars: dict[str, tk.IntVar] = {}

        self._box_param = {} if box_param is None else box_param

        self.button = Button(self, text = text, font = font, command=self.drop_value, **combo_param)
        self.button.place(x=0, y=0)
        self.button.update()

        self.configure(width=self.button.winfo_width(), height=self.button.winfo_height())

    def drop_value(self):
        if self._box.winfo_ismapped():
            self._box.place_forget()
        else:
            self._box.place(x=self.master.winfo_x()+self.winfo_x(), y=self.winfo_height()+self.winfo_y()+5, width = self.winfo_width())

    def add_selected(self, name: str):
        if name in self._selected.children:
            return

        selected = Button(self._selected, text=name.upper(), name=name, font=(self._font[0], self._font[1]-2), background=SECONDARY_COLOR, radius=10, width=len(name.upper())+2)
        selected.pack(side = tk.LEFT, anchor=tk.W, pady=2)
        selected.configure(command=lambda n = name: self.remove_selected(n, True))

    def remove_selected(self, name, is_click = False):
        self._selected.children[name].destroy()

        if is_click:
            self._checkVars[name].set(0)

        if name != 'all':
            return

        for _, var in self._checkVars.items():
            var.set(0)

    def check_cmd(self, name):
        var = self._checkVars[name]

        if self._checkVars['all'].get():
            self._checkVars['all'].set(0)
            self.remove_selected('all')
            for key, var in self._checkVars.items():
                if key in ['all', name]:
                    continue
                self.add_selected(key)
                self._checkVars[key].set(1)
            return

        if var.get():
            self.add_selected(name)
        else:
            self.remove_selected(name)

    def all_check_cmd(self):
        name = 'all'
        var = self._checkVars[name]

        for child in self._selected.winfo_children():
            try:
                if child.winfo_name() == name:
                    continue
                self.remove_selected(child.winfo_name())
            except:
                pass

        if var.get():
            self.add_selected(name)
            for key, var in self._checkVars.items():
                if key == name:
                    continue
                var.set(1)
        else:
            self.remove_selected(name)
            for key, var in self._checkVars.items():
                if key == name:
                    continue
                var.set(0)

    def set_drop_down_var(self, dropdown: DropDown):
        for child in dropdown._widgets:
            if type(child) is tk.Checkbutton:
                tempVar = tk.IntVar()
                tempVar.set(1)
                child.configure(variable=tempVar, command=lambda name=child.winfo_name(): self.check_cmd(name))
                self._checkboxes.append(child)
                self._checkVars[child.winfo_name()] = tempVar
            else:
                self.set_drop_down_var(child)

    def render_values(self):
        for value in self._values:
            if type(value) is dict:
                value: dict = value
                value.update({'background': self._box.cget('background')})
                temp = DropDown(self._box, **value)
                temp.pack(anchor = tk.NW)
                self.set_drop_down_var(temp)
            else:
                value: str = value
                tempVar = tk.IntVar()
                tempVar.set(1)
                temp = tk.Checkbutton(self._box, text = value.upper(),
                                      font = self._font,
                                      variable=tempVar,
                                      background=self._box.cget('background'),
                                      activebackground=self._box.cget('background'),
                                      selectcolor=self._box.cget('background'),
                                      name = value,
                                      command=lambda name=value: self.check_cmd(name))
                temp.pack(anchor = tk.NW)
                self._checkboxes.append(temp)
                self._checkVars[value] = tempVar

        if self._checkVars['all'].get():
            self._box.children['all'].configure(command=self.all_check_cmd)
            self.add_selected('all')


    def pack(self, **kwargs):
        super().pack(**kwargs)

        self.update_idletasks()
        if self._show_selected:
            self._selected = tk.Frame(self.master, width=100, height=self.button.winfo_height())
            self._selected.place(x=self.winfo_x()+self.winfo_width(), y=self.winfo_y())

        self._box = tk.Frame(self.master.master.master, height=self.winfo_height(), highlightthickness=1, highlightbackground='black', **self._box_param)

        self.render_values()