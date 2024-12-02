import asyncio
import Client

class Server:
    async def __init__(self, host, port):
        self.server = await asyncio.start_server(self.connection, host, port)
        self.unlogged = []
        self.socks = []

        async with self.server:
            await self.server.serve_forever()

    def connection(self, reader, writer):
        self.unlogged.append(Client(reader, writer))

        self.receive(self.unlogged[-1])

    async def send(self, sock, message):
        await sock.send(message)

    async def receive(self, sock):
        received = await sock.receive()

        i = received.find(" ")

        mtype = received[0]
        code = received[1:i]
        if i != -1:
            message = received[i+1:]

        # Respond to messages
        if mtype == "u" and message:
            self.send(self.socks[code], message)
        elif mtype == "$" and code == "chat":
            # message of form:
            # u_id timestamp
            options = message.split()

            # sqlite chats between sock.id & options[0]
            # collect messages with timestamp > options[1]
        elif mtype == "$" and code == "log":
            # message of form:
            # username password
            options = message.split()

            # sqlite find account with user & pass
            account = ""

            if account:
                u_id = 0

                # Remove sock from unlogged list
                self.unlogged.remove(sock)

                # set sock id to u_id

                # Add sock to logged list
                self.socks[u_id] = sock

            # respond "u_id color" or "none"
            asyncio.create_task(self.send(sock, account))
        
        asyncio.create_task(self.receive(self, sock))

    def get_socks(self):
        return self.socks
    
    def get_socks(self, index):
        return self.socks[index]