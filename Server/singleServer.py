#!/usr/bin/env python

import socket
import sys
import threading
import time
import queue as Queue
import select
from msgFrame import *

NUMBERS_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue.Queue()

inputs = []
outputs = []
message_queues = {}

terminals = []

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

        print("Host IP :" + host)
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
                #clients[str(list(connection.getpeername()))]=connection

            elif s in terminals:
                print("Terminal read")
                data = s.recv(1024)
                if data:
                    pass
            
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
                    #del clients[str(list(s.getpeername()))]
                    s.close()
                    del message_queues[s]

        for s in writable:

            if s in terminals:
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
            #del clients[str(list(s.getpeername()))]
####    /select event loop    ####





####    shell   ####

def start_shell():
    s1, s2 = socket.socketpair() # create AF_UNIX socket
    global terminal_socket
    terminal_socket = s1 # keep socket to communicate
    terminal_peer = s2 # add socket to TCP server
    terminals.append(terminal_peer)
    inputs.append(terminal_peer)

    while True:
        cmd = input('server>')

        if cmd == 'list':
            list_connections()

        elif 'echo' in cmd:
            echo_message(cmd)

        # TODO: add 'select all' feature   
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)

        elif cmd == '':
            continue
        else:
            print("bad command or filename")    

def echo_message(cmd):
    action = cmd.replace('echo ', '')
    terminal_socket.sendall(str.encode(action+"\n"))

# Display all current active connection with the clients

def list_connections():
    results = ''
    #all_connections = inputs
    print("connection size: " + str(len(inputs)))
    for i, conn in enumerate(inputs):
        try:
            if (conn is server) or (conn is terminal):
                continue
            print("pinging " + str(i))

            #conn.send(str.encode(' '))
            #conn.recv(201480)

            #send_message(conn, "ping")
            msg = createMessage("ping","request",conn.getpeername())
            b_msg = encode(msg)
            terminal_socket.sendall(b_msg)
            wait_for_message()

        except:
            print("ping failed to user")
            del inputs[i]
            if conn in outputs:
                outputs.remove(conn)
            #del all_addresses[i]
            continue
        
        results = str(i) + "     " + str(inputs[i].getpeername()[0]) + "     " + str(inputs[i].getpeername()[1]) + "\n"

    print("---- Clients ----")
    print("-ID-------IP--------PORT--------PING----")
    print(results)


    # Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target) # cast to int
        conn = inputs[target]
        print("you are now connected to " + str(inputs[target].getpeername()[0]))
        print(str(inputs[target].getpeername()[0]) +":"+ str(inputs[target].getpeername()[1]) + ">", end="") # format prompt

        return conn

        # 192.168.0.4>

    except:
        print("Selection not valid")
        return None


# Sends commands to client 
def send_target_command(conn):
    while True:
        try:
            cmd = input()
            if cmd == 'quit':
                #conn.close()
                #s.close()
                #sys.exit()
                break
            if len(str.encode(cmd)) > 0:
                #print(cmd)
                #hello_msg = "what's up??\n"
                #conn.sendall(hello_msg.encode())
                

                msg = cmd+"\n"
                #send_message(conn, msg)
                #conn.sendall(msg)



                #str.encode(cmd+"\n")
                message_queues[conn].put(str.encode("test\n"))
                if conn not in outputs:
                    outputs.append(conn)
                



                #client_response = str(conn.recv(20480),"utf-8")
                #print(client_response, end="")
        except:
            print("Bad command or file name")
            break

####    /shell   ####






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

        print(f"{clientSocket.getpeername()}>{msgType}: {msgMessage}")
        #print(jsonObj)

        #response = messageTypes["request"]["ping"](clientSocket)
        response = messageTypes[msgType][msgMessage](clientSocket)


        #server.sendall(response)
        clientSocket.sendall(response)



### reqs ###
def ping(clientSocket):
    msg = createMessage("pong","response","")
    b_msg = encode(msg)
    return b_msg

requests = {
    "ping":ping
}

### responses ###
def pong(clientSocket):
    pass
responses = {
    "pong":pong
}

### types ###
messageTypes = {
    "request":requests,
    "response":responses
}

####    /DB ####










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
        if x == 1: # handle connection
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2: # send commands - start shell
            start_shell()

        queue.task_done()

# Create jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()

## main ##
create_workers()
create_jobs()