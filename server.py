import asyncio
import client

class server:
    async def __init__(self, host, port):
        self.server = await asyncio.start_server(self.connection, host, port)
        self.socks = []

        async with self.server:
            await self.server.serve_forever()

    def connection(self, reader, writer):
        self.socks.append(client(reader, writer))

    async def send(self, sock, message):
        await sock.send(message)

    async def receive(self, index):
        return await self.socks[index].receive()
    
    async def receive_all(self):
        for sock in self.socks:
            asyncio.create_task(sock.receive())

    def get_socks(self):
        return self.socks
    
    def get_socks(self, index):
        return self.socks[index]