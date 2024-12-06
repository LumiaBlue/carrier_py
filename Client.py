import asyncio
from tkinter import StringVar

from Sock import Sock
from Window import Window

config = open("config.txt")
HOST = config.readline().split()[1]
PORT = config.readline().split()[1]
USER = config.readline().split()[1]
PASSW = config.readline().split()[1]
config.close()

win = Window()
win.master.title("Carrier")

users = {}
listbox_opts = StringVar(value="test")
win.create_widgets(listbox_opts)

class Client:
    def __init__(self):
        self.sock = None
        
        self.color = "blue"

    async def establish(self):
        print("establishing")
        reader, writer = await asyncio.open_connection(HOST, PORT)

        self.sock = Sock(reader, writer)
        asyncio.create_task(self.send(f"$log {USER} {PASSW}"))
        asyncio.create_task(self.send(f"a {USER}"))
        asyncio.create_task(self.receive())

    async def send(self, message):
        await self.sock.send(message)

    async def receive(self):
        received = await self.sock.receive()

        if not received:
            return
        asyncio.create_task(self.receive())

        i = received.find(" ")

        mtype = received[0]
        
        code = received[1:i]
        if i != -1:
            message = received[i+1:]
        
        if mtype == "m" and message:
            i = message.find(" ")

            s_id = int(message[0:i])
            text = message[i+1:]

            win.append_message(text, s_id)

        elif mtype == "a":
            accounts = message.split(",")[:-1]

            names = ""
            for account in accounts:
                uname = account.split()[0]
                uid = int(account.split()[1])

                users[uname] = uid
                names = names + " " + uname
            
            win.set_users(users)
            listbox_opts.set(names)

        elif mtype == "$" and code == "chat":
            splits = message.split(", ", 3)

            s_id = int(splits[0][1:])
            r_id = int(splits[1])

            text = splits[3][1:-2]

            if s_id == self.sock.id:
                win.append(text)
            else:
                win.append_message(text, s_id)
        elif mtype == "$" and code == "log":
            if message[0] == "F":
                print("logon failed")
                exit()
            else:
                self.sock.id = int(message.split()[0])
                self.color = message.split()[1]

        elif mtype == "$" and code == "exit":
            self.sock.__del__()

async def main():
    client = Client()
    await client.establish()

    win_task = asyncio.create_task(win.run_tk())
    win.set_sock(client.sock)

    await win_task

asyncio.run(main())
