import tkinter as tk

root = tk.Tk()

button = tk.Button(width=10, height=10)

root.rowconfigure(0, weight=1, pad=5)
root.columnconfigure(0, weight=1, pad=5)

button.grid(sticky=tk.N+tk.S+tk.E+tk.W)

tk.mainloop()