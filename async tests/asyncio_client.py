import asyncio

HOST = "127.0.0.1"
PORT = 65432

async def handle(reader, writer):
    active = [True]

    task = asyncio.create_task(send(writer, active))
    while True:
        data = (await reader.read(1024)).decode()

        if (reader.at_eof() or not active[0]):
            task.cancel()
            writer.close()
            return

        print(f"Received: {data}")

async def send(writer, active):
    while True:
        mess = await asyncio.to_thread(input)

        print(f"Sent: {mess}")
        writer.write(mess.encode())
        await writer.drain()

        if mess == "exit" or not active[0]:
            active[0] = False
            writer.close()
            return

async def run_server():
    reader, writer = await asyncio.open_connection(HOST, PORT)

    await handle(reader, writer)
    

asyncio.run(run_server())