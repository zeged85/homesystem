import asyncio
from aioconsole import ainput

clients = {}

class Client():
    def __init__(self,transport):
        self.transport=transport


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        clients[transport]=Client(transport)

    def data_received(self, data):
        asyncio.ensure_future(handleDataReceived(self, data))
        #await handleDataReceived(self,data)
        #peername = self.transport.get_extra_info('peername')
        #message = data.decode()
        ##print('Data received: {!r}'.format(message))
        #print(f"{peername}: {data}")
        ##print(self.)
#
        ##print('Send: {!r}'.format(message))
        #self.transport.write(data)
#
        ##print('Close the client socket')
        ##self.transport.close()

    def connection_lost(self, exc):
        peername = self.transport.get_extra_info('peername')
        print(f'client {peername} closed the connection')
        #print(self.transport.get_extra_info('socket').getpeername())
        #self.on_con_lost.set_result(True)


async def handleDataReceived(self,data):
    await asyncio.sleep(1)
    print("in data recevied")

async def send_message():
    while True:
        await asyncio.sleep(0.01)
        messageToSend = await ainput()
        print(messageToSend)
        if messageToSend == 'quit':
            print("quitting!")
        elif messageToSend == 'list':
            print("listing")
            #soc = transport.get_extra_info('socket')
            for client in clients:
                transport = clients[client].transport
                peername = transport.get_extra_info('peername')
                #ping =
                print()
                transport.write(b'ping')
                
            
        elif 'echo' in messageToSend:
            transport.write(messageToSend[5:].encode())
    


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    #srvClass = EchoServerProtocol()

    global server
    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        'localhost', 8888)

    #async with server:
    #    await server.serve_forever()

    await asyncio.gather(
        server.serve_forever(),
        send_message()
    )

try:
    asyncio.run(main())
except asyncio.exceptions.CancelledError:
    pass