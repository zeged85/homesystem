#!/usr/bin/env python

#ref: https://www.youtube.com/watch?v=6jteAOmdsYg&list=PLhTjy8cBISErYuLZUvVOYsR1giva2payF
#ref: https://github.com/mayankgureja/fullDuplexTCPChatServerClient/blob/master/fullDuplexTCPChatServer.py
#ref: https://steelkiwi.com/blog/working-tcp-sockets/


import socket
import sys

import threading
import time
import queue as Queue

import select

import json

import db as DB
from msgFrame import * #encode, decode, createMessage, address_to_bytes, bytes_to_address


NUMBERS_OF_THREADS = 3
JOB_NUMBER = [1, 2, 3]
#queue = Queue()
queue = Queue.Queue()
#all_connections = []
#all_addresses = []

#inputs = [server]
inputs = []
outputs = []
message_queues = {}

#lock = threading.Lock() 

#HEADERSIZE = 20

clients = {}

import ipaddress


#lock.acquire()
#lock.release()


#server_available = threading.Event()
#server_available.wait()
#server_available.set()


# get host public ip
def getHost():
    global host
    host = ""
    #try:
    #    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #    s.connect(('10.255.255.255', 8765)) # random addr. to resolve real see ref: https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    #    host = s.getsockname()[0]
    #    #print(s.getsockname()[0])
    #    s.close()
    #except:
    #    print("can't get real ip")
    #finally:
    #    s.close()


# Create a socket (connet two computers)
def create_socket():
    try:
        global host
        global port
        global server
        port = 10006
        #server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = socket.socket()
    except socket.error as msg:
        print("Socket creation error:" + str(msg))

# Binding the socket and listening for connections
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
        print("Socket binding error:" + str(msg) + "\n" + "Retrying...")
        exit()
        #bind_socket()



# Handling connection from multiple cilents and saving to list
# Closing previous connections when server.py file is restarted

def accepting_connection():
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        #lock.acquire()
           
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
                #msg = f"welcome to the server"
                #obj = {
                #    "message":msg,
                #    "type":"response"
                #}
                #jsonObj = json.dumps(obj)
                #rep = f'{len(jsonObj):<10}' + jsonObj
                #connection.send(bytes(rep,"utf-8"))

                # add to clients dictionary
                clients[str(list(connection.getpeername()))]=connection
                #print(f"adding {str(list(connection.getpeername()))} to clients dic")

            elif s is terminal:
                print("Terminal read")
                data = s.recv(1024)
                if data:
                    pass

            elif s is db:
                print("SRV: DB>client")
                data = s.recv(1024)
                if data:
                    print(data)

                    b_address = data[:ADDRESSSIZE]
                    ip, port = bytes_to_address(b_address)
                    #print(clients)
                    print(f"['{ip}', {port}]")
                    clientAddress = f"['{ip}', {port}]"
                    clientSocket =  clients[clientAddress]

                    #print(f"got my socket {clientSocket.getpeername()}")

                    clientMsgQueue =  message_queues[clientSocket]
                    clientMsgQueue.put(data[ADDRESSSIZE:])
                    if clientSocket not in outputs:
                        outputs.append(clientSocket)

                else: # Client left / ubruptly?
                
                    print("DEBUG: Client " + str(s.getpeername()) + " left!")
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del clients[str(list(s.getpeername()))]
                    s.close()
                    del message_queues[s]


            else:
                data = s.recv(1024)
                if data:
                    print(f"message from {s.getpeername()}")
                    address = s.getpeername()
                    
                    b_ip, b_port = address_to_bytes(address)
                    #print(f"ip : {b_ip}")
                    #print(f"len of ip is {len(b_ip)}")
                    #print(f"port : {b_port}")
                    #print(f"len of port is {len(b_port)}")
                    #ip, port = bytes_to_address(b_ip+b_port)
                    #print(f"after ip : {ip}")
                    #print(f"after port : {port}")

                    preamble = b_ip + b_port


                       
       
                    #print(f"address length {len(bytes(s.getpeername()))}")
                    #print(f'{bytes(s.getpeername())}')
                    message_queues[db].put(preamble + data)
                    if db not in outputs:
                        outputs.append(db)
                    #message_queues[s].put(data) # Ak - Automatic replay to clients sending a message
                    #if s not in outputs:
                    #    outputs.append(s)
                    '''
                    print(str(s.getpeername()) + " :", data)
                    try:
                        y = json.loads(data)
                        print(y)
                        try:
                            print(y['message'])
                            if y['message']=="ping":
                                print(f"terminal wants server to ping " + str(y['target']))
                                ping = {
                                    "message":"ping",
                                    "type":"request",
                                }
                                JsonObj = json.dumps(ping)
                                target = y['target']
                                print(f"looking for {str(target)} in {clients.keys()}")

                                msg = JsonObj
                                rep = f'{len(msg):<10}' + msg

                                c = clients[str(target)]
                                c.sendall(bytes(rep,"utf-8"))

                        except KeyError as err:
                            print("ERROR: JSON key not found:")
                            print(err)  


                        try:
                            print(y['type'])
                            
                        except KeyError as err:
                            print("ERROR: JSON key not found:")
                            print(err)  


                        
                    except json.JSONDecodeError as err:
                        print("ERROR: JSON Parse fail:",err)
                        #print(err)
                    '''
                   

                else: # Client left / ubruptly?
                
                    print("DEBUG: Client " + str(s.getpeername()) + " left!")
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    del clients[str(list(s.getpeername()))]
                    s.close()
                    del message_queues[s]
                    
    
        for s in writable:

            if s is terminal:
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

        #lock.release()
        #print("a")
        #print("",flush=True)
        #print("server>",end="", flush=True)














#    for c in all_connections:
#        c.close()
#
#    del all_connections[:]
#    del all_addresses[:]
#
#
#    while True:
#        try:
#            conn, address = s.accept()
#            s.setblocking(1) # prevents timeout
#
#            all_connections.append(conn)
#            all_addresses.append(address)
#
#            print("connection has been established : " + address[0])
#
#        except:
#            print("ERROR accepting connection")





# Data to JSON to Dictionary
def dataToDic(data):
    try:
        jsonStr = json.loads(data)

    except json.JSONDecodeError as err:
        print("ERROR: JSON Parse fail:")
        print(err)

# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# ClientID, name
# 0 friend-A
# 1 friend-B
# 2 friend-C

# custom shell
def start_turtle():

    # create AF_UNIX socket
    s1, s2 = socket.socketpair()
    global terminal
    
    
    # add socket to TCP server
    terminal = s2
    inputs.append(terminal)

    # keep socket to communicate
    global terminal_socket
    terminal_socket = s1

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
            print("command not recognized")



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
            print("Error sending commands")
            break


#def send_message(conn, message):
#    #lock.acquire()
#    ##conn.sendall(str.encode(message))
#    toSendObj = {
#        "message":"ping",
#        "type":"request",
#        "target":conn.getpeername()
#    }
#    toSendJson = json.dumps(toSendObj)
#    terminal_socket.sendall(bytes(toSendJson,"utf-8"))
#    #lock.release()

def wait_for_message():
    print("terminal waiting for ping reply")
    data = terminal_socket.recv(2048)
    print("terminal recvd msg")
    jsonObj = json.loads(data)

    print(jsonObj)


# Create DB
# bind socket
def create_db():

    # create AF_UNIX socket
    s1, s2 = socket.socketpair()
    s1.setblocking(0)
    s2.setblocking(0)
    global db
    
    
    # add socket to TCP server
    db = s2
    inputs.append(db)
    message_queues[db] = Queue.Queue()

    # keep socket to communicate
    global db_api
    db_socket = s1

    db_api = DB.db(db_socket)

    

def start_db():
    db_api.start()

    

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
            getHost()
            create_socket()
            bind_socket()
            accepting_connection()
        if x == 2: # send commands - start shell
            start_turtle()
        if x == 3: # start DB
            create_db()
            start_db()

        queue.task_done()


# Create jobs
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()






create_workers()
create_jobs()


## Establish connection with client (socket must be listening)
#def socket_accept():
#    conn, address = s.accept()
#    print("Connection has been established! |" + " IP " + address[0] + " | Port " + str(address[1]))
#    hello_msg = "welcome client!\n"
#    conn.sendall(hello_msg.encode())
#    hello_msg = "what's up??\n"
#    conn.sendall(hello_msg.encode()) 
#    send_commands(conn)
#    conn.close()
#

#
#def main():
#    create_socket()
#    bind_socket()
#    socket_accept()
#
#main()
