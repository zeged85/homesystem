#!/usr/bin/env python

#ref: https://github.com/mayankgureja/fullDuplexTCPChatServerClient/blob/master/fullDuplexTCPChatServer.py
import socket
import select


def runSelect():
    selectUnsucessful = True
    while selectUnsucessful:
        try:
            readyRecvList, readySendList, readyErrList = select.select(recvList, sendList, [])
            selectUnsucessful = False
        except select.error:
            for fd in recvList:
                try:
                    tempRecvList, tempSendList, tempErrList = select.select([fd], [], [], 0)
                except select.error:
                    if fd == serverSocket:
                        fd.close()
                        exit(1)
                    else:
                        if fd in recvList:
                            recvList.remove(fd)
                        fd.close()
    return readyRecvList, readySendList

def handleListeningSocket():
    try:
        newConnectionSocket, addr = serverSocket.accept()
    except socket.error as err:
        print("\nERROR: something went wrong in the accept() function call:", err)
        exit(1)
    
    try:
        recvList.append(newConnectionSocket)
        sendList.append(newConnectionSocket)
        
        print("INFO: Connecting socket created between " +str(newConnectionSocket.getsockname())+" and " + str(newConnectionSocket.getpeername()))
        print("* Client "+ str(newConnectionSocket.getpeername()) +" is ready *")
    except (socket.error, socket.gaierror) as err:
        print("\nERROR: Something went wrong with the new connection socket:", err)
        if newConnectionSocket in recvList:
            recvList.remove(newConnectionSocket)
            sendList.remove(newConnectionSocket)
        newConnectionSocket.close()

def handleConnectedSocket():
    try:

        recvIsComplete = False
        rcvdStr = ""

        while not recvIsComplete:
            rcvdStr = rcvdStr + fd.recv(1024)

            if fd not in sendList:
                sendList.append(fd)

            # ~ is the delimiter used to indicate message start and finish
            if rcvdStr.strip('~') != "":
                if (rcvdStr[0] == "~") and (rcvdStr[-1] == "~"):
                    recvIsComplete = True
                    clientMessage = rcvdStr.strip('~')
            else: # if empty string, connection has been terminated
                if fd in recvList:
                    recvList.remove(fd)

                if fd in sendList:
                    sendList.remove(fd)

                del clientMessages[fd] # delete connection information
                fd.close()

        if clientMessage == "quit()":
            print("\n* Client " + str(fd.getpeername()) + " has left *\n")

            if fd in recvList:
                recvList.remove(fd)
                fd.close()

            if fd in sendList:
                sendList.remove(fd)
                fd.close()
        
        else:
            print("\n" + fd.getpeername() + ": " + clientMessage)
            clientMessages[fd] = str(clientMessage) # add message to dictionary, pending transmission

    except socket.error as err:
        print("\nERROR: Connection to client has abruptly ended:" + err)
        if fd in recvList:
            recvList.remove(fd)
        if fd in sendList:
            sendList.remove(fd)
        fd.close()
        print("* I am ready to chat w/ new client! *\n")


# main

# Global Variables
serverHost = ""
serverPort = 2222
recvList = []
sendList = []
clientMessages = {}

try:
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setblocking(0)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSocket.bind((serverHost,serverPort))
    serverSocket.listen(3)

    print("INFO: I am listening at " + str(serverSocket.getsockname()))
    print("* I am ready to chat w/ new client! *\n")

except (socket.error, socket.gaierror) as err:
    print("\nERROR: Something went wrong in creating the listening socket:" + err)
    exit(1)

recvList = [serverSocket]

try:
    while True:
        serverSocket.setblocking(False)
        readyForRecv, readyForSend = runSelect()

        for fd in readyForRecv:
            if fd == serverSocket:
                handleListeningSocket()
            else:
                handleConnectedSocket()

        for fd in readyForSend:
            try:
                broadcast = ""
                if fd in clientMessages.keys(): # See if connection information exists
                    broadcast = str(clientMessages[fd]) # Add message to broadcast variable
                
                if broadcast != "": # See if message is actually there
                    for client in readyForSend: # Broadcast message to every connected client
                        if broadcast != "":
                            print("* Broadcasting message \"" + str(broadcast) + "\" to " + str(clientMessages.getpeername()))
                            client.send(str(fd.getpeername() + ": " + str(broadcast)))

                    clientMessages[fd] = "" # Empty pending messages
            
            except:
                print("\nERROR: Something awful happened while broadcasting messages")
                break

except socket.error as err:
    print("\nERROR: Something awful happened with a connected socket:" + err)

    if fd in recvList:
        recvList.remove(fd)
    
    if fd in sendList:
        sendList.remove(fd)

    fd.close()

except KeyboardInterrupt:
    for fd in recvList:
        fd.close()

    print("\nINFO: KeyboardInterrupt")
    print("* Closing all sockets and exiting... Goodbye! *")
    exit(0)


        