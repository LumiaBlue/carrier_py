import asyncio 
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

async def initialize():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((HOST, PORT))
    client_sock.setblocking(False)
    
    
    task = asyncio.create_task(receive(client_sock))
    await send(client_sock)

    client_sock.close()
    task.cancel()

    return True

async def receive(conn):
    loop = asyncio.get_event_loop()
    while True:
        data = await loop.sock_recv(conn, 1024)

        print(f"Received: {data.decode()}")

async def send(conn):
    while True:
        mess = await asyncio.to_thread(input)

        if mess == "exit":
            return
        else:
            print(f"Sent: {mess}")
            conn.sendall(mess.encode())
    


asyncio.run(initialize())