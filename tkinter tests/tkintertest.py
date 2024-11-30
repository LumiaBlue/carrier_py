import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()

contacts = tk.Listbox(root, width = 20, height = 23)
output = scrolledtext.ScrolledText(root, width = 40, height = 20)
entry = tk.Entry(root, width = 40)

contacts.grid(rowspan= 2, column=0)
output.grid(row = 0, column = 1)
entry.grid(row = 1, column = 1)

def send(event):
    output.configure(state = tk.NORMAL)
    output.insert(tk.INSERT, entry.get() + "\n")
    output.configure(state = tk.DISABLED)
    entry.delete(0, tk.END)

entry.bind('<Return>', send)
output.configure(state = tk.DISABLED)

tk.mainloop()

print("test")