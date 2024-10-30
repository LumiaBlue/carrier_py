import tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()

output = scrolledtext.ScrolledText(root, width = 40, height = 20)
entry = tk.Entry(root, width = 40)

output.grid(row = 0, column = 0)
entry.grid(row = 1, column = 0)

def send(event):
    output.configure(state = tk.NORMAL)
    output.insert(tk.INSERT, entry.get() + "\n")
    output.configure(state = tk.DISABLED)
    entry.delete(0, tk.END)

entry.bind('<Return>', send)
output.configure(state = tk.DISABLED)

tk.mainloop()

print("test")