#!/usr/bin/env python
print("trd")
import select, socket, sys
import queue as Queue

print("trd")

PORT = 10010

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
print("binding on port: " + str(PORT))
try:
    server.bind(('', PORT))
except socket.error as msg:
    print("Socket binding error:" + str(msg) + "\n" + "Retrying...")
    exit()

server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            print("connection has been established : " + client_address[0])
            print("INFO: Connecting socket created between " +str(connection.getsockname())+" and " + str(connection.getpeername()))
            print("* Client "+ str(connection.getpeername()) +" is ready *")
            connection.setblocking(0)
            inputs.append(connection)
            message_queues[connection] = Queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                #message_queues[s].put(data) # Ak - Automatic replay to clients sending a message
                #if s not in outputs:
                #    outputs.append(s)
                print(str(s.getpeername()) + " :", data)
            else: # Client left / ubruptly?

                print("DEBUG: Client " + str(s.getpeername()) + " left!")
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except Queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)

    for s in exceptional:
        print("ERROR: removing " + str(connection.getpeername()))
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
