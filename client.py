import asyncio
import Sock

config = open("config.txt")
HOST = config.readline().split()[1]
PORT = config.readline().split()[1]
USER = config.readline().split()[1]
PASSW = config.readline().split()[1]
config.close()

class Client:
    async def __init__(self):
        reader, writer = await asyncio.open_connection(HOST, PORT)

        self.sock = Sock(reader, writer)
        self.color = "blue"

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

            # Print to application
            # if s_id == self.sock.id you:
            # else name:
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