import asyncio

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

class Client:
    def __init__(self):
        self.sock = None
        
        self.color = "blue"

    async def establish(self):
        print("establishing")
        reader, writer = await asyncio.open_connection(HOST, PORT)

        self.sock = Sock(reader, writer)
        asyncio.create_task(await self.send(f"$log {USER} {PASSW}"))
        asyncio.create_task(await self.receive())

    async def send(self, message):
        await self.sock.send(message)

    async def receive(self):
        received = await self.sock.receive()

        i = received.find(" ")

        mtype = received[0]
        
        code = received[1:i]
        if i != -1:
            message = received[i+1:]
        
        if mtype == "m" and message:
            sender = message.split()[0]

        elif mtype == "$" and code == "chat":
            splits = message.split(" ", 5)

            name = splits[0]

            sender = splits[1]
            recip = splits[2]

            if sender == self.sock.id:
                win.append(message[-1])
            else:
                win.append(message[-1], name)
        elif mtype == "$" and code == "log":
            if message[0] == "F":
                print("logon failed")
                exit()
            else:
                self.sock.id = message.split()[0]
                self.color = message.split()[1]

        elif mtype == "$" and code == "exit":
            self.sock.__del__()
        
        asyncio.create_task(await self.receive())

async def main():
    client = Client()

    asyncio.create_task(client.establish())
    win_task = asyncio.create_task(win.run_tk())

    await win_task

asyncio.run(main())