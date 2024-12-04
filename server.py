import sqlite3
import asyncio
import time

import Sock

conn = sqlite3.connect("carrier.db")
cur = conn.cursor()

class Server:
    async def __init__(self, host, port):
        self.server = await asyncio.start_server(self.connection, host, port)
        self.unlogged = []
        self.socks = []

        async with self.server:
            await self.server.serve_forever()
    
    def __del__(self):
        for sock in self.unlogged:
            sock.__del__()
        
        for sock in self.socks():
            sock.__del__()

    def connection(self, reader, writer):
        self.unlogged.append(Sock(reader, writer))

        asyncio.create_task(self.receive(self.unlogged[-1]))

    async def send(self, sock, message):
        await sock.send(message)

    async def sendall(self, sock, messages):
        for message in messages:
            await sock.send(message)
        
        await sock.send("$end")

    async def receive(self, sock):
        received = await sock.receive()

        # Find index of first spacce
        i = received.find(" ")

        # Find Type code (u, $, etc)
        mtype = received[0]

        # message code (chat, log, etc)
        code = received[1:i]
        if i != -1:
            message = received[i+1:]

        # Respond to messages
        if mtype == "u" and message:
            self.send(self.socks[code], message)

            cur.execute(f"INSERT INTO MESSAGES VALUES (?,?,?,?)", (sock.uuid, code, message, time.time(),))
            conn.commit()
        elif mtype == "$" and code == "chat":
            # message of form:
            # u_id timestamp
            options = message.split()

            # sqlite chats between sock.id & options[0]
            r_id = cur.execute(f"SELECT * FROM Users WHERE uname == {options[0]} LIMIT 1").fetchone()
            messages = cur.execute(f"SELECT * FROM Messages WHERE s_id == {sock.id} and r_id == {r_id[0]} ORDER BY time ASC").fetchall()
            # collect messages with timestamp > options[1]
            asyncio.create_task(self.sendall(sock, messages))
            
        elif mtype == "$" and code == "log":
            # message of form:
            # username password
            options = message.split()

            # sqlite find account with user & pass
            account = cur.execute(f"SELECT * FROM Users WHERE uname == {options[0]} AND pass == {options[1]}")

            if account:
                # Remove sock from unlogged list
                self.unlogged.remove(sock)

                # set sock id to u_id
                sock.id = account[0]

                # Add sock to logged list
                self.socks[account[0]] = sock

                # respond to client
                asyncio.create_task(self.send(sock, f"$log T {account[2]}"))
            else:
                asyncio.create_task(self.send(sock, f"$log F"))            
        
        asyncio.create_task(self.receive(self, sock))

    def get_socks(self):
        return self.socks
    
    def get_socks(self, index):
        return self.socks[index]