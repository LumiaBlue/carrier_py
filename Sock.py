import asyncio

class Sock:
    def __init__(self, reader, writer):
        self.id = -1
        self.reader = reader
        self.writer = writer
    
    def __del__(self):
        self.writer.close()

    async def receive(self):
        data = (await self.reader.read(1024)).decode()

        if (self.reader.at_eof()):
            self.__del__()
            return None

        return data

    async def send(self, message):
        self.writer.write(message.encode())
        await self.writer.drain()
    
        if (message == "$exit"):
            self.__del__()