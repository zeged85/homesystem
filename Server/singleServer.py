#!/usr/bin/env python

import socket
import sys
import threading
import time
import queue as Queue
import select
from msgFrame import *
import shell

NUMBERS_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue.Queue()

inputs = []
outputs = []
message_queues = {}

global terminal_socket



clients = {}

####    init TCP socket ####
def create_socket():
    try:
        global host
        global port
        global server
        host = ""
        port = 10006
        #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = socket.socket()
    except socket.error as msg:
        print("Socket creation error:" + str(msg))

def bind_socket():
    try:
        global host
        global port
        global server

        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        print("Binding the port:" + str(port))

        #print("Host IP :" + host)
        server.bind((host,port))
        server.listen(5)
        inputs.append(server)

    except socket.error as msg:
        print("Socket binding error:" + str(msg))
        exit()
####    /init TCP socket    ####

####    select event loop   ####
def accepting_connection():
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for s in readable:
            if s is server:
                connection, client_address = s.accept()
                print("connection has been established : " + client_address[0])
                print("INFO: Connecting socket created between " +str(connection.getsockname())+" and " + str(connection.getpeername()))
                print("* Client "+ str(connection.getpeername()) +" is ready *")
                connection.setblocking(0)
                inputs.append(connection)
                message_queues[connection] = Queue.Queue()

                # welcome message

                msg = createMessage("welcome to the server", "response","")
                obj = encode(msg)
                connection.send(obj)

                # add to clients dictionary
                clients[str(list(connection.getpeername()))]=connection

            elif s is terminal_socket:
                #print("Terminal read")
                data = s.recv(1024)
                if data:
                    handleTerminal(data)
                    #print(data)
            
            else:
                data = s.recv(1024)
                if data:
                    print(f"message from {s.getpeername()}")  

                    handleMessage(s, data)

                else: # Client left / ubruptly?
                
                    print("DEBUG: Client " + str(s.getpeername()) + " left!")
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del clients[str(list(s.getpeername()))]
                    s.close()
                    del message_queues[s]

        for s in writable:

            if s is terminal_socket:
                print("Terminal write")

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
            del clients[str(list(s.getpeername()))]
####    /select event loop    ####



####    DB  ####

def handleMessage(clientSocket , message):
        jsonObj = decode(message[MESSAGESIZE:])
        try:
            msgType = jsonObj['type']
        except KeyError as err:
            print(f"KeyError: {err.args[0]}")
            response = encode(createMessage("keyError","response",err.args[0]))
            
            clientSocket.sendall(response)
            return


        msgMessage = jsonObj['message']

        msgArgs = jsonObj['args']

        print(f"{clientSocket.getpeername()}>{msgType}: {msgMessage}")
        #print(jsonObj)

        #response = messageTypes["request"]["ping"](clientSocket)
        try:
            messageTypes[msgType][msgMessage](clientSocket)
        except KeyError as err:
            print(f"KeyError: {err.args[0]}")
            response = encode(createMessage("keyError","response",err.args[0]))
            
            clientSocket.sendall(response)
            return

        #server.sendall(response)
        #clientSocket.sendall(response)





def pingClient(idx):

    print("pinging " + idx)
    #t = time.time()
#
    #msg = createMessage("ping","request",str(list(conn.getpeername())))
    #b_msg = encode(msg)
    #terminal_socket.sendall(b_msg)
    #wait_for_message()
    #elapsed = time.time() - t
    #ping = round(elapsed,4)



### reqs ###
def ping(clientSocket):
    #if 
    msg = createMessage("pong","response","")
    b_msg = encode(msg)
    #clientSocket.sendall(b_msg)
    message_queues[clientSocket].put(b_msg)
    if clientSocket not in outputs:
        outputs.append(clientSocket)

requests = {
    "ping":ping
}

### responses ###
def pong(clientSocket):
    print("ponging b to terminal")
    msg = createMessage("pong","response",str(list(clientSocket.getpeername())))
    b_msg = encode(msg)
    terminal_socket.sendall(b_msg) 

responses = {
    "pong":pong
}

### types ###
messageTypes = {
    "request":requests,
    "response":responses
}

####    /DB ####

 # Display all current active connection with the clients

def list_connections(self):
    results = ''
    #all_connections = inputs
    print("connection size: " + str(len(inputs)))
    for i, conn in enumerate(inputs):
        try:
            if (conn is server) or (conn is terminal_socket):
                continue
            print("pinging " + str(i))
            t = time.time()
            msg = createMessage("ping","request",str(list(conn.getpeername())))
            b_msg = encode(msg)
            terminal_socket.sendall(b_msg)
            wait_for_message()
            elapsed = time.time() - t
            ping = round(elapsed,4)
            #print(f"elapsed: {ping}")
        except Exception as err:
            print("ping failed to user")
            print(err)
            del inputs[i]
            if conn in outputs:
                outputs.remove(conn)
            #del all_addresses[i]
            continue
        
        results += f" {str(i-1)}     {str(inputs[i].getpeername()[0])}     {str(inputs[i].getpeername()[1])}    {str(ping)}ms  \n"
    print("---- Clients ----")
    print("-ID-------IP--------PORT--------PING----UP-TIME----")
    print(results)


####    terminal handler    ####
def handleTerminal(data):
    cmd = str(data,"utf-8")
    print(f"handling {cmd}")
    


    if "ping" in cmd:
        idx = cmd[5:]
        print(f"should ping {idx}")
        pingClient(idx)

        #print(clients[oArgs])
        #try:
        #    #print(clients[oArgs])
        #    conn = clients[oArgs]
        #except KeyError as err:
        #    print(f"KeyError: {err}")
        #else:
        #    print("am i sending ping?")
        #    msg = createMessage("ping","request","")
        #    b_msg = encode(msg)
        #    message_queues[conn].put(b_msg)
        #    if conn not in outputs:
        #        outputs.append(conn)
    
    
    else:
        print("Bad command or file name")
        


####    /terminal handler   ####



####    shell   ####


def create_shell():


   s1, s2 = socket.socketpair() # create AF_UNIX socket
   global terminal_socket
   terminal_socket = s1 # keep socket to communicate
   terminal_peer = s2 # add socket to TCP server
   ##terminals.append(terminal_socket)
   inputs.append(terminal_socket)


   myShell = shell.shell(terminal_peer)
   myShell.start_shell()



####    /shell   ####

####    init    ####

# Create worker threads
def create_workers():
    for _ in range(NUMBERS_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

# Do next jobs that is in the queue (handle connections, send commands)
def work():
    while True:
        x = queue.get()
        if x == 2: # handle connection
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 1: # send commands - start shell
            create_shell() # shell first - needs terminal in inputs before

        queue.task_done()

# Create jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

## main ##
create_workers()
create_jobs()