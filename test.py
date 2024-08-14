import tkinter as tk

def on_focus(event):
    # Change the border color when the canvas is focused
    canvas.config(highlightbackground="blue", highlightthickness=2)

def on_focus_out(event):
    # Reset the border color when focus is lost
    canvas.config(highlightbackground="lightgray", highlightthickness=0)

# Create the main window
root = tk.Tk()

# Create a canvas
canvas = tk.Canvas(root, width=200, height=200, bg="white",
                   highlightbackground="lightgray", highlightthickness=0)

# Bind focus and focus out events to the canvas
canvas.bind("<FocusIn>", on_focus)
canvas.bind("<FocusOut>", on_focus_out)

# Make the canvas focusable
canvas.configure(takefocus=True)

# Pack the canvas
canvas.pack(pady=20)

# Create some buttons
button1 = tk.Button(root, text="Button 1")
button1.pack(pady=10)

button2 = tk.Button(root, text="Button 2")
button2.pack(pady=10)

# Run the application
root.mainloop()
