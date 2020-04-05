#!/usr/bin/env python
"""
fullDuplexTCPChatClient.py
Mayank Gureja
01/31/2013
ECEC 433
ref: https://github.com/mayankgureja/fullDuplexTCPChatServerClient/blob/master/fullDuplexTCPChatClient.py
"""



import socket
import select
import sys

import json
from msgFrame import *

#HEADERSIZE = 10

#from msgFrame import createMessage, decode, encode




def main():
    """
    main - Runs the Full Duplex Chat Client
    """
    global clientSocket

    serverHost = 'localhost'
    serverPort = 10006

    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print("ERROR: Cannot create client side socket:", err)
        exit(1)

    while True:
        try:
            clientSocket.connect((serverHost, serverPort))
        except socket.error as err:
            print("ERROR: Cannot connect to chat server", err)
            print("* Exiting... Goodbye! *")
            exit(1)
        except:
            print("ERROR: Something awful happened!")
            exit(1)
        break

    recvList = [clientSocket, sys.stdin]

    print(f"* Connected to server {clientSocket.getpeername()} as {clientSocket.getsockname()} *") 

    print("client>",end="", flush=True)
    try:
        while True:
            readyRecvList, readySendList, readyErrList = select.select(recvList, [], [])

            for fd in readyRecvList:
                if fd == sys.stdin:
                    message = sys.stdin.readline().rstrip()

                    if (message == ''):
                        print("client>",end="", flush=True)
                        continue

                    
                    msg = createMessage(message, "request","")
                    enc = encode(msg)
                    clientSocket.sendall(enc)

                    if (message == "quit()"):
                        print("* Exiting chat room! *")
                        clientSocket.close()
                        exit(0)
                        break
                    print("client>",end="", flush=True)

                elif fd == clientSocket:
                    clientSocket.settimeout(3)
                    try:
                        message = clientSocket.recv(2048)
                    except socket.timeout as err:
                        print("ERROR: The recv() function timed out after 3 seconds! Try again.")
                    except:
                        print("ERROR: Something awful happened!")
                    else:
                        if message == "" or message == b'':
                            print("server closed the connection")
                            for fd in recvList:
                                fd.close()
                                exit(1)
                            break
                        else:
                            #print (f"{message}\n")

                            handleMessage(message)


                    clientSocket.settimeout(None)
                    break
            #print("client>",end="", flush=True)

    except select.error as err:
        for fd in recvList:
            try:
                tempRecvList, tempSendList, tempErrList = select.select([fd], [], [], 0)
            except select.error:
                if fd == clientSocket:
                    fd.close()
                    exit(1)
                else:
                    if fd in recvList:
                        recvList.remove(fd)
                        fd.close()

    except socket.error as err:
        print("ERROR: Cannot connect to chat server", err)
        print ("* Exiting... Goodbye! *")
        exit(1)

        if fd in recvList:
            fd.close()

    except KeyboardInterrupt:
        print("\nINFO: KeyboardInterrupt")
        print("* Closing all sockets and exiting chat server... Goodbye! *")
        clientSocket.close()
        exit(0)



def handleMessage(message):
    #msg_len = int(message[:MESSAGESIZE])
    #print(f'message length {msg_len}')
    jsonObj = decode(message[MESSAGESIZE:])
    print()
    print(f"Server> {jsonObj['type']}: {jsonObj['message']}")
    
    msgType = jsonObj['type']
    msgMessage = jsonObj['message']
    
    response = messageTypes[msgType][msgMessage]
    response()
def ping():
    msg = createMessage("pong","response","")
    enc = encode(msg)
    clientSocket.sendall(enc)

requests = {
    "ping":ping
}

def pong():
    print("pong!")

def welcome():
    print("welcome!")

def keyError():
    print("keyError!")

responses = {
    "pong":pong,
    "welcome to the server":welcome,
    "keyError":keyError
}

messageTypes = {
    "request":requests,
    "response":responses
}

if __name__ == '__main__':
    main()