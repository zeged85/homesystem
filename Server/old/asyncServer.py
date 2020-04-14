import asyncio
from aioconsole import ainput

async def handle_echo(reader, writer):
    while True:
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
    
        print(f"Received {message!r} from {addr!r}")
    
        print(f"Send: {message!r}")
        writer.write(data)
        await writer.drain()
    
        #print("Close the connection")
        #writer.close()




async def send_message():
    while True:
        await asyncio.sleep(0.01)
        messageToSend = await ainput()
        print(messageToSend)





async def main():
    server = await asyncio.start_server(
        handle_echo, 'localhost', 10006)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    #async with server:
    #    await server.serve_forever()

    await asyncio.gather(
        server.serve_forever(),
        send_message()
    )


asyncio.run(main())