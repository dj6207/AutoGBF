import tkinter as tk

#get mouse position
def mouse_position():
    x, y = root.winfo_pointerx(), root.winfo_pointery()
    position_label.config(text="Mouse position: ({}, {})".format(x, y))
    root.after(100, mouse_position)

root = tk.Tk()
root.title("Mouse Position Tracker")

position_label = tk.Label(root, text="Mouse position:")
position_label.pack()

root.after(100, mouse_position)

root.mainloop()
