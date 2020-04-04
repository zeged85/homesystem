import asyncio
import socket
import os # filesize


async def handleDataReceived(self,loop,data):
    peername = self.transport.get_extra_info('peername')
    message = data.decode().rstrip()
    print(f"{peername}>{message}")
    await asyncio.sleep(1)
    print("in data recevied")
    if message == 'download':

        result = await loop.run_in_executor(None, blocking_io,self)
        print('default thread pool', result)
        #blocking_io()

def blocking_io(self):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_address = ('10.0.0.41', 0)
        print("starting up on ",server_address[0]," port ",server_address[1])
        sock.bind(server_address)
    except socket.error as msg:
        print("Socket creation error:" + str(msg))
    port = sock.getsockname()[1]
    #resp = bytes(f"port {port}\n","utf-8")
    #self.transport.write(resp)  
  
    
   
    sock.listen(1)
    

        
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('shared/wallpaper.jpg', 'rb') as f:
        fileSize = os.fstat(f.fileno()).st_size
        print(fileSize)
        resp = bytes(f"port {port} size {fileSize}\n","utf-8")
        self.transport.write(resp)


        print(f"waiting for a connection on port:{port}")
        connection, client_address = sock.accept()
        print("connection from:", client_address)


        data = f.read(100)
        #print(data)



        while data:
        #hello_msg = "welcome client!"
            connection.sendall(data)
            data = f.read(100)
    
    #connection.shutdown(socket.SHUT_WR)
    connection.shutdown(2)
    connection.close()
    sock.close()