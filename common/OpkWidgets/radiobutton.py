import tkinter as tk

class RadioButton(tk.Canvas):
    def __init__(self, parent, text, variable, value, radius=10, **kwargs):
        super().__init__(parent, width=200, height=30, bg="white", highlightthickness=0)
        self.variable = variable
        self.value = value
        self.radius = radius

        # Create the circle (radio button)
        self.circle = self.create_oval(10, 10, 10 + 2 * radius, 10 + 2 * radius, outline="black", width=2)

        # Create the text label next to the circle
        self.label = self.create_text(10 + 3 * radius, 10 + radius, text=text, anchor=tk.W)

        # Bind click event to toggle selection
        self.bind("<Button-1>", self.on_click)
        self.tag_bind(self.circle, "<Button-1>", self.on_click)
        self.tag_bind(self.label, "<Button-1>", self.on_click)

        # Update the display based on the variable's value
        self.update_display()

    def on_click(self, event=None):
        self.variable.set(self.value)
        self.update_display()

    def update_display(self):
        if self.variable.get() == self.value:
            self.itemconfig(self.circle, fill="black")  # Filled circle for selected
        else:
            self.itemconfig(self.circle, fill="white")  # Empty circle for unselected