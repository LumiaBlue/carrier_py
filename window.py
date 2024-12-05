import tkinter as tk
from tkinter import scrolledtext
import asyncio

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.create_widgets()
    
    @asyncio.coroutine
    def run_tk(root, interval=0.05):
        try:
            while True:
                root.update()
                yield from asyncio.sleep(interval)
        except tk.TclError as e:
            if "application has been destroyed" not in e.args[0]:
                raise

    def create_widgets(self):
        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=8)

        contact_frame = tk.LabelFrame(self, text=" Contacts ", padx=2)
        self.contacts = tk.Listbox(contact_frame, width = 20)

        contact_frame.rowconfigure(0, weight=1)
        contact_frame.columnconfigure(0, weight=1)
        contact_frame.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.contacts.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.contacts.pack(fill=tk.BOTH, expand=True)

        message_frame = tk.Frame(self)
        message_frame.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        message_frame.rowconfigure(1, weight=1)
        message_frame.columnconfigure(0, weight=1)

        self.create_io(message_frame)

    def create_io(self, parent):
        self.chatter = tk.StringVar(value="No Active Chat")
        chat_label = tk.Label(parent, textvariable=self.chatter, width=45, anchor=tk.W, padx=5)

        self.output = scrolledtext.ScrolledText(parent, width = 40, height = 20)
        
        self.input = tk.StringVar()
        entry = tk.Entry(parent, width = 40, textvariable=self.input)

        chat_label.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.output.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        entry.grid(row=2, column=0, padx=4, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.output.tag_config("m")
        self.output.tag_config("i", foreground="blue")
        self.output.tag_config("o", foreground="red")

        def send(event):
            self.append(self.input.get())
            self.input.set("")

        entry.bind('<Return>', send)
        self.output.configure(state = tk.DISABLED)

    def append(self, text, sender=None):
        self.output.configure(state=tk.NORMAL)

        if not sender:
            self.output.insert(tk.END, "you: ", "i")
        else:
            self.output.insert(tk.END, "sender: ", "o")
        
        self.output.insert(tk.END, text + "\n", "m")
        self.output.configure(state = tk.DISABLED)

    def append_light(self, text, sender=None):
        if not sender:
            self.output.insert(tk.END, "you: ", "i")
        else:
            self.output.insert(tk.END, "sender: ", "o")
        
        self.output.insert(tk.END, text + "\n", "m")

    def update_chat(self, self_id, target_name, messages):
        # Clear current chat from output
        self.chatter.set(target_name)
        self.output.configure(state=tk.NORMAL)
        self.output.delete(0, tk.END)
        self.input.set("")

        for message in messages:
            if message[0] != self_id:
                self.append_light(message[2], target_name)
            else:
                self.append_light(message[2])

        self.output.configure(state=tk.DISABLED)