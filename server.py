import sqlite3
import asyncio
import time

from Sock import Sock

conn = sqlite3.connect("carrier.db")
cur = conn.cursor()

config = open("server_config.txt")
HOST = config.readline().split()[1]
PORT = config.readline().split()[1]
config.close()

class Server:
    def __init__(self):
        num_accs = cur.execute("SELECT count(*) FROM Users").fetchone()
        self.unlogged = []
        self.socks = [None] * (num_accs[0] + 1)

    async def establish(self, host, port):
        self.server = await asyncio.start_server(self.connection, host, port)

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
            await sock.send(f"$chat {message}")
            await asyncio.sleep(0.1)

    async def receive(self, sock):
        received = await sock.receive()
        if not received:
            return

        asyncio.create_task(self.receive(sock))

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
            if self.socks[int(code)]:
                asyncio.create_task(self.send(self.socks[int(code)], f"m {sock.id} {message}"))

            cur.execute(f"INSERT INTO MESSAGES VALUES (?,?,?,?)", (sock.id, code, time.time(), message,))
            conn.commit()
        elif mtype == "a":
            accounts = cur.execute("SELECT uname, uid FROM Users WHERE uname != (?)", (message,)).fetchall()

            response = "a "
            for account in accounts:
                response = response + account[0] + " "  + str(account[1]) + ","
            
            asyncio.create_task(self.send(sock, response))
        elif mtype == "$" and code == "chat":
            # message of form:
            # uname
            options = message.split()

            # sqlite chats between sock.id & options[0]
            r_id = cur.execute("SELECT * FROM Users WHERE uname == (?) LIMIT 1", (options[0],)).fetchone()
            messages = cur.execute('''SELECT * FROM (SELECT * FROM 
                                   (SELECT * FROM Messages WHERE s_id == (?) AND r_id == (?) 
                                   UNION 
                                   SELECT * FROM Messages WHERE r_id == (?) AND s_id == (?)) 
                                   ORDER BY timestamp DESC LIMIT 5) ORDER BY timestamp ASC''', (sock.id, r_id[0], sock.id, r_id[0],)).fetchall()
            
            if messages:
                asyncio.create_task(self.sendall(sock, messages))
            
        elif mtype == "$" and code == "log":
            # message of form:
            # username password
            options = message.split()

            # sqlite find account with user & pass
            account = cur.execute("SELECT * FROM Users WHERE uname == (?) AND pass == (?)", (options[0], options[1],)).fetchone()

            if account:
                # Remove sock from unlogged list
                self.unlogged.remove(sock)

                # set sock id to u_id
                sock.id = account[0]

                # Add sock to logged list
                self.socks[account[0]] = sock

                # respond to client
                asyncio.create_task(self.send(sock, f"$log {account[0]} {account[2]}"))
            else:
                asyncio.create_task(self.send(sock, f"$log F")) 
        elif mtype == "$" and code == "exit":
            sock.__del__()

    def get_socks(self):
        return self.socks
    
    def get_socks(self, index):
        return self.socks[index]

async def main():
    server = Server()

    await server.establish(HOST, PORT)

asyncio.run(main())